#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
把 iOS-App-Analysis 项目打包成可推送到 GitHub 的归档目录。

设计目标：
  - 每个文件都低于 GitHub 的 50 MB 提示线（硬上限 100 MB）
  - 两个大 IPA 按固定字节数切片，附自动下载 + 合并 + 校验工具
  - 全程只读源目录，不改动原项目
  - 生成 archive-manifest.json / SHA256SUMS.txt 供机器与人工核对

用法：
  python build_github_archive.py --dst <克隆仓库目录>/ios-app-analysis
"""

import argparse
import hashlib
import json
import os
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path

SRC = Path(r"E:\iOS-App-Analysis")
CHUNK = 48_000_000  # 48 MB 十进制，低于 GitHub 50 MB 警告线
RAW_BASE = ("https://raw.githubusercontent.com/Xuefeng122/talang-files/"
            "main/ios-app-analysis/")

# (源相对路径, 归档相对路径)
SMALL_FILES = [
    # 文档
    ("README.md", "docs/00-项目总览.md"),
    ("03-Analysis/分析说明.md", "docs/01-分析说明与保留记录.md"),
    ("03-Analysis/分析报告.md", "docs/02-分析报告与环境核验.md"),
    ("03-Analysis/技术教程.md", "docs/03-看懂一个IPA-技术教程.md"),
    ("01-IPA/下载说明.md", "docs/04-夸克归档与通道实测.md"),
    ("04-Theos-Project/README.md", "docs/05-Theos工程说明.md"),
    # 脚本
    ("build_github_archive.py", "scripts/build_github_archive.py"),
    ("03-Analysis/macho_inspect.py", "scripts/macho_inspect.py"),
    ("03-Analysis/deep_inspect.py", "scripts/deep_inspect.py"),
    ("03-Analysis/run-analysis.sh", "scripts/run-analysis.sh"),
    ("03-Analysis/makefile-note.txt", "scripts/makefile-note.txt"),  # 可选，不存在会跳过
    ("01-IPA/fetch_ipa.py", "scripts/fetch_ipa.py"),
    # Theos / Logos 工程骨架
    ("04-Theos-Project/Makefile", "scripts/theos/Makefile"),
    ("04-Theos-Project/control", "scripts/theos/control"),
    ("04-Theos-Project/ResearchKit.plist", "scripts/theos/ResearchKit.plist"),
    ("04-Theos-Project/RKSettings.h", "scripts/theos/RKSettings.h"),
    ("04-Theos-Project/RKSettings.m", "scripts/theos/RKSettings.m"),
    ("04-Theos-Project/RKPanel.h", "scripts/theos/RKPanel.h"),
    ("04-Theos-Project/RKPanel.m", "scripts/theos/RKPanel.m"),
    ("04-Theos-Project/Tweak.x", "scripts/theos/Tweak.x"),
    # 包内清单（有价值的独立信息，不含二进制）
    ("02-Extracted/Soul/_ziplist.txt", "reports/bundle-listing/Soul_ziplist.txt"),
    ("02-Extracted/MOMO/_ziplist.txt", "reports/bundle-listing/MOMO_ziplist.txt"),
]

# 整目录复制：源相对目录 -> 归档相对目录 -> 允许的扩展名
REPORT_DIRS = [
    ("03-Analysis/target-reports", "reports/deep", {".json", ".md"}),
    ("03-Analysis/reports", "reports/structure", {".json", ".md"}),
    ("03-Analysis/sample-report", "reports/sample", {".json", ".md"}),
]

# (源 IPA, 还原后的 ASCII 文件名, 展示用原始文件名)
IPAS = [
    ("01-IPA/Soul_6.41.0.ipa", "Soul_6.41.0.ipa", "Soul_6.41.0.ipa"),
    ("01-IPA/MOMO陌陌_9.23.2.ipa", "MOMO_9.23.2.ipa", "MOMO陌陌_9.23.2.ipa"),
]


def sha256_file(path: Path):
    h = hashlib.sha256()
    size = 0
    with open(path, "rb") as f:
        while True:
            b = f.read(1024 * 1024)
            if not b:
                break
            h.update(b)
            size += len(b)
    return h.hexdigest(), size


def human(n: int) -> str:
    for unit in ("B", "KB", "MB", "GB"):
        if n < 1024 or unit == "GB":
            return f"{n:.1f} {unit}" if unit != "B" else f"{n} B"
        n /= 1024.0


def put(safe_copy, src: Path, rel: str, entries: list):
    if not src.is_file():
        return False
    dst = safe_copy(src, rel)
    digest, size = sha256_file(dst)
    entries.append({"path": rel, "size": size, "sha256": digest})
    return True


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dst", required=True, help="归档输出目录")
    ap.add_argument("--clean", action="store_true", default=True)
    args = ap.parse_args()

    dst = Path(args.dst)
    if args.clean and dst.exists():
        shutil.rmtree(dst)
    dst.mkdir(parents=True, exist_ok=True)

    def safe_copy(src: Path, rel: str) -> Path:
        out = dst / rel
        out.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, out)
        return out

    entries = []

    # 1) 小文件
    skipped = []
    for s, d in SMALL_FILES:
        if not put(safe_copy, SRC / s, d, entries):
            skipped.append(s)

    # 2) 报告目录
    for sdir, ddir, exts in REPORT_DIRS:
        p = SRC / sdir
        if not p.is_dir():
            skipped.append(str(sdir))
            continue
        for f in sorted(p.rglob("*")):
            if f.is_file() and f.suffix.lower() in exts and "__pycache__" not in f.parts:
                rel = f"{ddir}/{f.name}"
                put(safe_copy, f, rel, entries)

    # 3) 两个 IPA 分卷
    ipa_dir = dst / "ipa-parts"
    ipa_dir.mkdir(parents=True, exist_ok=True)
    originals = []
    for src_rel, out_name, display in IPAS:
        src = SRC / src_rel
        if not src.is_file():
            print(f"[WARN] 缺少 IPA：{src}", file=sys.stderr)
            continue
        digest, total = sha256_file(src)
        parts = []
        idx = 0
        with open(src, "rb") as f:
            while True:
                buf = f.read(CHUNK)
                if not buf:
                    break
                idx += 1
                pname = f"{out_name}.part{idx:03d}"
                ppath = ipa_dir / pname
                with open(ppath, "wb") as w:
                    w.write(buf)
                ph, ps = sha256_file(ppath)
                rel = f"ipa-parts/{pname}"
                entries.append({"path": rel, "size": ps, "sha256": ph})
                parts.append({"name": pname, "size": ps, "sha256": ph,
                              "url": RAW_BASE + "ipa-parts/" + pname})
        originals.append({
            "output": out_name,
            "display_name": display,
            "size": total,
            "sha256": digest,
            "part_count": idx,
            "parts": parts,
        })
        print(f"[分卷] {display}: {human(total)} -> {idx} 片")

    # 4) 归档级元数据骨架
    manifest = {
        "schema": "ios-app-analysis/archive-v1",
        "created_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "source": str(SRC),
        "chunk_bytes": CHUNK,
        "raw_base": RAW_BASE,
        "originals": originals,
        "files": [],
    }
    INDEX_NAMES = ("README.md", "manifest.md", "index.html")

    # 5) 归档级 Git 属性 + 还原工具
    # -text 让所有文件按字节入仓，避免 Windows CRLF 转换导致 SHA256SUMS.txt 校验失败
    (dst / ".gitattributes").write_text(
        "# 本目录所有文件按字节存储，禁止换行转换，保证 SHA256SUMS.txt 跨平台可校验\n"
        "* -text\n", encoding="utf-8", newline="\n")
    (dst / "restore.py").write_text(RESTORE_PY, encoding="utf-8", newline="\n")
    (dst / "restore.ps1").write_text(RESTORE_PS1, encoding="utf-8", newline="\n")
    (dst / "IPA_ORIGINAL_HASHES.txt").write_text(
        "\n".join(f"{o['sha256']}  {o['output']}  (原始文件 {o['display_name']}, "
                  f"{o['size']} B)" for o in originals) + "\n",
        encoding="utf-8", newline="\n")

    # 6) 收集所有普通文件（排除机器清单、哈希清单、三份索引文档）
    files = []
    for f in sorted(dst.rglob("*")):
        if not f.is_file() or "__pycache__" in f.parts:
            continue
        rel = f.relative_to(dst).as_posix()
        if rel in ("archive-manifest.json", "SHA256SUMS.txt") or rel in INDEX_NAMES:
            continue
        digest, size = sha256_file(f)
        files.append({"path": rel, "size": size, "sha256": digest})

    # 7) 三份索引文档（内容引用的是「不含自身」的清单，避免自引用哈希循环）
    doc_view = dict(manifest, files=files)
    (dst / "README.md").write_text(build_readme(doc_view), encoding="utf-8", newline="\n")
    (dst / "manifest.md").write_text(build_manifest_md(doc_view), encoding="utf-8", newline="\n")
    (dst / "index.html").write_text(build_index(doc_view), encoding="utf-8", newline="\n")
    for name in INDEX_NAMES:
        p = dst / name
        digest, size = sha256_file(p)
        files.append({"path": name, "size": size, "sha256": digest})

    # 8) 写机器清单（不含自身）与标准哈希清单（含机器清单，不含自身）
    manifest["files"] = files
    (dst / "archive-manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8", newline="\n")
    mh, ms = sha256_file(dst / "archive-manifest.json")
    with open(dst / "SHA256SUMS.txt", "w", encoding="utf-8", newline="\n") as w:
        for e in sorted(files, key=lambda x: x["path"]):
            w.write(f"{e['sha256']}  {e['path']}\n")
        w.write(f"{mh}  archive-manifest.json\n")

    total_size = sum(e["size"] for e in files) + ms
    print(f"\n[完成] {len(files) + 2} 个文件，合计 {human(total_size)}")
    print(f"[输出] {dst}")
    if skipped:
        print("[跳过（源不存在）] " + ", ".join(skipped))


# ---------------------------------------------------------------- 生成文档

def build_readme(m: dict) -> str:
    rows = "\n".join(
        f"| `{o['output']}` | {human(o['size'])} | {o['part_count']} | "
        f"`{o['sha256'][:16]}…` |" for o in m["originals"])
    return f"""# iOS 应用结构分析工作台 · GitHub 归档

归档时间：{m['created_utc']}　来源：`{m['source']}`
本目录是 2026-11-09 ~ 11-10 建立的分析项目的完整交付副本，与根目录原有的 WCRefine 资料包相互独立。

---

## 01 · IPA 分卷（重点）

GitHub 单文件硬上限 100 MB，两个 IPA 分别 220 MB / 165 MB，因此按 **{m['chunk_bytes']:,} B（48 MB）** 原始字节切片，**不做二次压缩**（IPA 内部已是压缩数据，再压几乎不减小体积）。

| 还原后文件 | 原始大小 | 分卷数 | 原始 SHA-256（前 16 位） |
| --- | ---: | ---: | --- |
{rows}

> `MOMO_9.23.2.ipa` 是 `MOMO陌陌_9.23.2.ipa` 的 ASCII 别名，字节内容完全一致，还原后想用原名自行改名即可。

### 还原方式（三选一）

```bash
# A. 已有全部分卷，本地合并 + 校验（需 Python 3，无需第三方库）
python restore.py

# B. 只有这一个脚本，自动从本仓库下载全部分卷再合并
python restore.py --download

# C. Windows PowerShell（无需 Python）
powershell -ExecutionPolicy Bypass -File restore.ps1
```

`restore.py` 会逐片校验 SHA-256，合并后再次核对整个 IPA 的哈希；任一字节不符即报错退出。`IPA_ORIGINAL_HASHES.txt` 另存了原始哈希，可独立复核。

## 02 · 目录结构

| 目录 | 内容 |
| --- | --- |
| `ipa-parts/` | 两个 IPA 的 48 MB 分卷（共 {sum(o['part_count'] for o in m['originals'])} 片） |
| `docs/` | 项目总览、分析说明与保留记录、分析报告、技术教程、夸克通道实测、Theos 工程说明 |
| `scripts/` | `macho_inspect.py`、`deep_inspect.py`、`run-analysis.sh`、`fetch_ipa.py`，以及 `theos/` 下的完整 Logos/Theos 工程骨架 |
| `reports/` | 两层只读结构报告（JSON + Markdown）、REA 内容寻址证据图、样本报告、包内清单 |
| `restore.py` / `restore.ps1` | 分卷下载、合并、SHA-256 校验工具 |
| `archive-manifest.json` | 机器可读全量清单（每个文件路径、字节数、哈希） |
| `SHA256SUMS.txt` | 标准 `sha256sum -c` 格式清单 |
| `index.html` | 免登录直链下载页，列出每片分卷的完整 raw 地址 |

## 03 · 直链规则

把 `index.html` 里任一文件名接到下面的前缀后面，就是免登录可直接下载的 raw 直链：

```
{m['raw_base']}
```

例如：`{m['raw_base']}ipa-parts/Soul_6.41.0.ipa.part001`

## 04 · 未收录的内容

| 未收录 | 原因 |
| --- | --- |
| `02-Extracted/` 下解压出的主 Mach-O（合计约 440 MB） | 与 IPA 内容重复，可从分卷随时还原，重复上传无意义 |
| `02-Extracted/pipeline-sample/` 及其 IPA | 流水线验证用的无关第三方样本，不是本项目产出 |
| `__pycache__/`、临时日志 | 编译缓存与中间产物 |

原始项目保留了完整内容，本归档只是分发用的精简副本。

## 05 · 环境与能力边界（如实记录）

- REA 在本机 Windows 上只跑通了**包级证据图**：`open_binary` + `inspect_artifact` + `export_evidence_bundle`。Soul 12,108 项检查 / 3,919 节点 / 0 矛盾；陌陌 8,113 项检查 / 2,662 节点 / 0 矛盾。
- **函数级反编译未跑通**，且不是「没配后端」这么简单：Windows 版 Ghidra 明确拒绝 `mach-o / arm64`，Hopper 与 `inspect_macho` / `inspect_signature` 仅 macOS，IDA MCP 未注册、Kuna 未安装。要拿伪代码必须换 macOS / Linux。
- 「深度」部分由两个纯标准库只读解析器补齐：符号表、ObjC / Swift 节、代码签名 SuperBlob / CodeDirectory / entitlements、导出 trie、LINKEDIT 分区、Info.plist 与包内分布。
- Theos 工程骨架源码完整，`logos.pl` 展开与 `clang -fsyntax-only -target arm64-apple-ios16.5` 均零错误；但本机编不出 `.deb`（Windows 原生 make 取不到 `uname -s`，且缺 ldid 与 arm64 链接器），换 macOS / Linux / 配好工具链的 WSL 可直接 `make package`。

## 06 · 边界说明

- 全部内容来自用户本人提供的样本，分析过程**全程只读**：未修改 IPA、未写入宿主 App、未提取任何用户数据。
- 归档不含任何运行时注入、鉴权绕过、付费逻辑改写、广告或水印移除的实现，也不含定位或改写业务方法的步骤；`scripts/theos/` 只是设置面板 / 开关 / 日志的合规工程骨架。
- 报告只描述「文件里有什么」，不描述「怎么改变它的行为」。
- **IPA 为第三方商业应用的安装包，且本仓库为 public**：任何拿到链接的人都可下载。请仅用于个人本地研究与备份，遵守对应软件许可与所在地法规，不要二次分发或商用。文件版权归各自权利人所有。
- 若你把归档转发给他人，请自行评估上述风险；如不希望公开，可将本仓库转为 private 或删除 `ipa-parts/` 目录。

---

生成工具：`scripts/build_github_archive.py`（已收录，可在本归档基础上复现整套打包流程）
"""


def build_manifest_md(m: dict) -> str:
    groups = {}
    for e in sorted(m["files"], key=lambda x: x["path"]):
        top = e["path"].split("/")[0] if "/" in e["path"] else "（根目录）"
        groups.setdefault(top, []).append(e)
    out = [f"# 归档文件清单 · 共 {len(m['files'])} 个文件", "",
           f"生成时间：{m['created_utc']}　合计 {human(sum(e['size'] for e in m['files']))}\n"]
    for g, items in groups.items():
        out.append(f"\n## {g}（{len(items)} 个文件 / {human(sum(i['size'] for i in items))}）\n")
        out.append("| 文件 | 大小 | SHA-256（前 16 位） |")
        out.append("| --- | ---: | --- |")
        for i in items:
            out.append(f"| `{i['path']}` | {human(i['size'])} | `{i['sha256'][:16]}…` |")
    out.append("\n---\n\n上表为实体资料文件；`README.md`、`manifest.md`、`index.html` 三份索引文档及 "
               "`archive-manifest.json` 的哈希见 `SHA256SUMS.txt`（索引文件无法包含自身哈希）。\n"
               "机器可读清单见 `archive-manifest.json`。\n")
    return "\n".join(out)


CSS = """:root{--bg:#f5f6f8;--card:#fff;--ink:#16191d;--sub:#5c6672;--line:#e3e7ec;--accent:#1f9fa3;--accent-soft:#e6f6f6;--shadow:0 2px 18px rgba(20,30,40,.07)}
@media (prefers-color-scheme:dark){:root{--bg:#111418;--card:#1b2027;--ink:#eef1f4;--sub:#a2adb8;--line:#2c343d;--accent:#5cd0d2;--accent-soft:#1c3335;--shadow:0 2px 18px rgba(0,0,0,.3)}}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--ink);font:16px/1.65 -apple-system,BlinkMacSystemFont,"PingFang SC","Microsoft YaHei",sans-serif;-webkit-text-size-adjust:100%}
.wrap{max-width:760px;margin:0 auto;padding:40px 18px 64px}
header{text-align:center;margin-bottom:30px}
h1{font-size:22px;font-weight:650;margin:0 0 8px;letter-spacing:.02em}
.lead{color:var(--sub);font-size:14px;margin:0}
.badge{display:inline-block;margin-top:14px;padding:5px 12px;border-radius:999px;background:var(--accent-soft);color:var(--accent);font-size:12px;font-weight:600}
h2{font-size:16px;margin:28px 0 12px;font-weight:650}
.card{background:var(--card);border:1px solid var(--line);border-radius:16px;padding:18px 20px;box-shadow:var(--shadow);margin-bottom:12px}
.name{font-size:15px;font-weight:650;margin:0 0 4px;word-break:break-all}
.meta{color:var(--sub);font-size:13px;margin:0 0 12px}
.btn{display:inline-block;text-align:center;padding:9px 15px;border-radius:10px;background:var(--accent);color:#fff;text-decoration:none;font-weight:600;font-size:14px}
.btn.secondary{background:transparent;color:var(--accent);border:1px solid var(--accent);font-weight:500}
.url{margin-top:10px;padding:9px 11px;background:var(--bg);border:1px dashed var(--line);border-radius:9px;font:12px/1.5 ui-monospace,SFMono-Regular,Menlo,monospace;color:var(--sub);word-break:break-all;user-select:all}
.note{color:var(--sub);font-size:13px;line-height:1.85;margin:22px 0 0;padding:16px 18px;border-left:3px solid var(--accent);background:var(--card);border-radius:0 10px 10px 0}
code{background:var(--bg);padding:2px 5px;border-radius:4px;font-size:12px}
footer{text-align:center;color:var(--sub);font-size:12px;margin-top:30px}
"""


def build_index(m: dict) -> str:
    cards = []
    for o in m["originals"]:
        cards.append(f'<h2>{o["display_name"]} · {human(o["size"])} · {o["part_count"]} 片</h2>')
        for p in o["parts"]:
            cards.append(
                f'<div class="card"><p class="name">{p["name"]}</p>'
                f'<p class="meta">{human(p["size"])} · SHA256 <code>{p["sha256"][:16]}…</code></p>'
                f'<a class="btn" href="{RAW_BASE}ipa-parts/{p["name"]}" download>下载这一片</a>'
                f'<div class="url" data-raw="ipa-parts/{p["name"]}"></div></div>')
    part_html = "\n".join(cards)
    return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>iOS 应用结构分析 · 归档下载</title>
<style>
{CSS}</style>
</head>
<body>
<div class="wrap">
<header>
  <h1>iOS 应用结构分析工作台 · 归档</h1>
  <p class="lead">免登录直链 · 48 MB 分卷 · 自动还原与 SHA-256 校验</p>
  <div class="badge">2026-11-10 归档</div>
</header>

<div class="card">
  <p class="name">一键还原（推荐）</p>
  <p class="meta">下载 <code>restore.py</code>，运行 <code>python restore.py --download</code>，自动拉齐全部分卷、合并并校验哈希</p>
  <a class="btn" href="{RAW_BASE}restore.py" download>下载 restore.py</a>
  <a class="btn secondary" href="{RAW_BASE}README.md" target="_blank">查看归档说明</a>
  <a class="btn secondary" href="{RAW_BASE}manifest.md" target="_blank">查看完整清单</a>
</div>

{part_html}

<h2>其它资料</h2>
<div class="card">
  <p class="name">archive-manifest.json / SHA256SUMS.txt</p>
  <p class="meta">机器可读全量清单与标准哈希文件，用于离线校验</p>
  <a class="btn secondary" href="{RAW_BASE}archive-manifest.json" target="_blank">manifest.json</a>
  <a class="btn secondary" href="{RAW_BASE}SHA256SUMS.txt" target="_blank">SHA256SUMS.txt</a>
</div>

<div class="note">
  <strong>关于直链与还原</strong><br>
  上面每片分卷的灰色地址栏就是免登录 raw 直链，可直接复制转发；任何拿到链接的人都能下载。<br>
  分卷是原始字节切片，未二次压缩。合并顺序按 <code>.part001 → .part00N</code>，<code>restore.py</code> / <code>restore.ps1</code> 会逐片核对 SHA-256，合并后再核对整个 IPA 的哈希。<br>
  <strong>请注意</strong>：IPA 为第三方商业应用安装包，本仓库为 public，请仅用于个人本地研究与备份，遵守对应软件许可，不要二次分发或商用。
</div>

<footer>踏浪 · iOS 应用结构分析工作台 · 生成于 {m['created_utc']}</footer>
</div>
<script>
(function(){{
  var base="{RAW_BASE}";
  Array.prototype.forEach.call(document.querySelectorAll('.url[data-raw]'),function(e){{
    e.textContent=base+e.getAttribute('data-raw');
  }});
}})();
</script>
</body>
</html>
"""


RESTORE_PY = r'''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""iOS 应用结构分析归档 · 分卷下载 / 合并 / SHA-256 校验工具

用法:
    python restore.py                  # 从 ./ipa-parts/ 读取本地分卷并合并
    python restore.py --download        # 自动从 GitHub 下载缺失分卷再合并
    python restore.py --check          # 只校验分卷，不合并
    python restore.py --out DIR         # 指定输出目录（默认 ./）

仅使用 Python 标准库，跨平台。
"""
import argparse
import hashlib
import json
import os
import sys
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
MANIFEST = HERE / "archive-manifest.json"
PARTS_DIR = HERE / "ipa-parts"
DEFAULT_MANIFEST_URL = ("https://raw.githubusercontent.com/Xuefeng122/talang-files/"
                        "main/ios-app-analysis/archive-manifest.json")


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def fetch(url: str, dest: Path) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    tmp = dest.with_suffix(dest.suffix + ".downloading")
    print(f"  下载 {url}")
    try:
        with urllib.request.urlopen(url, timeout=120) as r, open(tmp, "wb") as w:
            total = int(r.headers.get("Content-Length") or 0)
            done = 0
            for chunk in iter(lambda: r.read(1024 * 1024), b""):
                w.write(chunk)
                done += len(chunk)
                if total:
                    print(f"\r  {done * 100 // total:3d}%  {done:,}/{total:,} B", end="", flush=True)
            if total:
                print()
        tmp.replace(dest)
    except Exception:
        if tmp.exists():
            tmp.unlink()
        raise


def main() -> int:
    ap = argparse.ArgumentParser(description="分卷下载 / 合并 / 校验")
    ap.add_argument("--download", action="store_true", help="自动下载缺失分卷")
    ap.add_argument("--check", action="store_true", help="只校验，不合并")
    ap.add_argument("--out", default=str(HERE), help="IPA 输出目录")
    ap.add_argument("--manifest", default=str(MANIFEST), help="清单路径")
    args = ap.parse_args()

    if not Path(args.manifest).is_file():
        if args.manifest == str(MANIFEST) and DEFAULT_MANIFEST_URL:
            print("未找到 archive-manifest.json，自动从仓库下载清单…")
            try:
                fetch(DEFAULT_MANIFEST_URL, MANIFEST)
            except Exception as exc:
                print(f"下载清单失败：{exc}", file=sys.stderr)
                return 2
        else:
            print(f"错误：找不到清单 {args.manifest}", file=sys.stderr)
            return 2
    m = json.loads(Path(args.manifest).read_text(encoding="utf-8"))
    base = m.get("raw_base", "")
    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)

    ok = True
    for o in m["originals"]:
        print(f"\n=== {o['display_name']} -> {o['output']} ===")
        verified = []
        for p in o["parts"]:
            f = PARTS_DIR / p["name"]
            if not f.is_file():
                if not args.download:
                    print(f"  缺少分卷 {f.name}" + ("（加 --download 自动下载）" if base else ""))
                    ok = False
                    continue
                if not base:
                    print("  清单里没有 raw_base，无法自动下载", file=sys.stderr)
                    return 2
                fetch(base + "ipa-parts/" + p["name"], f)
            actual = sha256(f)
            if actual != p["sha256"]:
                print(f"  ✗ {p['name']} 哈希不符\n    期望 {p['sha256']}\n    实际 {actual}")
                ok = False
                continue
            size = f.stat().st_size
            if size != p["size"]:
                print(f"  ✗ {p['name']} 大小不符：{size} != {p['size']}")
                ok = False
                continue
            print(f"  ✓ {p['name']}  {size:,} B")
            verified.append(f)
        if not ok or len(verified) != len(o["parts"]):
            print("  跳过合并（存在缺失或损坏的分卷）")
            continue
        if args.check:
            print("  --check 模式，仅校验完成")
            continue
        target = out_dir / o["output"]
        with open(target, "wb") as w:
            for f in verified:
                with open(f, "rb") as r:
                    for chunk in iter(lambda: r.read(1024 * 1024), b""):
                        w.write(chunk)
        final = sha256(target)
        if final != o["sha256"] or target.stat().st_size != o["size"]:
            print(f"  ✗ 合并结果哈希不符：{final}")
            ok = False
            continue
        print(f"  ✓ 还原完成：{target}  ({o['size']:,} B, SHA256 {final})")

    print("\n" + ("全部校验 / 还原成功。" if ok else "存在错误，请检查上面的输出。"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
'''


RESTORE_PS1 = r'''# iOS 应用结构分析归档 - 分卷合并与 SHA-256 校验（无需 Python）
# 用法: powershell -ExecutionPolicy Bypass -File restore.ps1
#       加 -Download 可自动从 GitHub 下载缺失分卷

param([switch]$Download)

$ErrorActionPreference = "Stop"
$Here = Split-Path -Parent $MyInvocation.MyCommand.Path
$Manifest = Join-Path $Here "archive-manifest.json"
$PartsDir = Join-Path $Here "ipa-parts"
$ManifestUrl = "https://raw.githubusercontent.com/Xuefeng122/talang-files/main/ios-app-analysis/archive-manifest.json"
if (-not (Test-Path $Manifest)) {
    Write-Host "archive-manifest.json not found, downloading..."
    Invoke-WebRequest -Uri $ManifestUrl -OutFile $Manifest -UseBasicParsing
}

$m = Get-Content $Manifest -Raw -Encoding UTF8 | ConvertFrom-Json
$base = $m.raw_base
$allOk = $true

foreach ($o in $m.originals) {
    Write-Host ""
    Write-Host "=== $($o.display_name) -> $($o.output) ==="
    $verified = @()
    foreach ($p in $o.parts) {
        $f = Join-Path $PartsDir $p.name
        if (-not (Test-Path $f)) {
            if (-not $Download) {
                Write-Host "  MISSING $($p.name)  (use -Download)"
                $allOk = $false
                continue
            }
            New-Item -ItemType Directory -Force -Path $PartsDir | Out-Null
            $url = $base + "ipa-parts/" + $p.name
            Write-Host "  downloading $url"
            Invoke-WebRequest -Uri $url -OutFile $f -UseBasicParsing
        }
        $actual = (Get-FileHash $f -Algorithm SHA256).Hash.ToLower()
        $size = (Get-Item $f).Length
        if ($actual -ne $p.sha256 -or $size -ne $p.size) {
            Write-Host "  FAIL $($p.name) hash/size mismatch"
            $allOk = $false
            continue
        }
        Write-Host "  OK $($p.name)  $size B"
        $verified += $f
    }
    if (-not $allOk -or $verified.Count -ne $o.parts.Count) {
        Write-Host "  skip merge (missing or damaged parts)"
        continue
    }
    $target = Join-Path $Here $o.output
    $stream = [System.IO.File]::Open($target, "Create", "Write")
    try {
        foreach ($f in $verified) {
            $bytes = [System.IO.File]::ReadAllBytes($f)
            $stream.Write($bytes, 0, $bytes.Length)
        }
    } finally { $stream.Close() }
    $final = (Get-FileHash $target -Algorithm SHA256).Hash.ToLower()
    if ($final -eq $o.sha256) {
        Write-Host "  RESTORED $target  ($($o.size) B)"
    } else {
        Write-Host "  FAIL merged hash mismatch"
        $allOk = $false
    }
}
Write-Host ""
if ($allOk) { Write-Host "All parts verified and restored." } else { Write-Host "Errors found."; exit 1 }
'''


if __name__ == "__main__":
    main()
