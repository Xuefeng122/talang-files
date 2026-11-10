#!/usr/bin/env python3
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
