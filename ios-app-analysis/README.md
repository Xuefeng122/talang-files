# iOS 应用结构分析工作台 · GitHub 归档

归档时间：2026-11-10T04:20:28Z　来源：`E:\iOS-App-Analysis`
本目录是 2026-11-09 ~ 11-10 建立的分析项目的完整交付副本，与根目录原有的 WCRefine 资料包相互独立。

---

## 01 · IPA 分卷（重点）

GitHub 单文件硬上限 100 MB，两个 IPA 分别 220 MB / 165 MB，因此按 **48,000,000 B（48 MB）** 原始字节切片，**不做二次压缩**（IPA 内部已是压缩数据，再压几乎不减小体积）。

| 还原后文件 | 原始大小 | 分卷数 | 原始 SHA-256（前 16 位） |
| --- | ---: | ---: | --- |
| `Soul_6.41.0.ipa` | 209.9 MB | 5 | `84497208f44b7cc4…` |
| `MOMO_9.23.2.ipa` | 157.6 MB | 4 | `fe86448b141057ee…` |

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
| `ipa-parts/` | 两个 IPA 的 48 MB 分卷（共 9 片） |
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
https://raw.githubusercontent.com/Xuefeng122/talang-files/main/ios-app-analysis/
```

例如：`https://raw.githubusercontent.com/Xuefeng122/talang-files/main/ios-app-analysis/ipa-parts/Soul_6.41.0.ipa.part001`

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
