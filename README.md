# WCRefine 版本包 + 反编译源码 · 打包清单

打包时间：2026-11-07
对象：**WCRefine**（`com.qimiao.WCRefine`，版本 **2.1-9**，rootless / arm64）

> 「wcr 版本与源码」按此理解：把 WCRefine 的**可安装版本包**和**函数级反编译源码**一并打包。
> 若你指的是别的东西（例如踏浪插件本体源码），告诉我，我另打一份。

---

## 01_版本包（可安装 / 版本信息）

| 文件 | 说明 |
| --- | --- |
| `WCRefine_2.1-9_无根.deb` | rootless deb 安装包，10.8 MB，原始分发包内取出 |
| `WCRefine.plist` | tweak 注入配置（Filter / Bundle） |
| `control.txt` | deb 控制信息：包名、版本 2.1-9、依赖 `firmware (>= 14.0), mobilesubstrate`、架构 `iphoneos-arm64` |
| `WCRefine_2.zip` | 原始分发 zip（WinZip AES-256 加密，密码 `1`），内容与上面的 deb 相同，仅作原始样本留存 |

## 02_反编译源码（重点）

| 文件 | 说明 |
| --- | --- |
| `WCRefine_full.txt` | **93.7 MB**，Ghidra 12.1.4 全函数反编译 C，**58,491 个函数**；每个函数前有 `/* ===== 函数名 @ 入口地址 ===== */` 标记 |
| `WCRefine_函数索引.txt` | 2.6 MB 索引：`源码行号 \| 入口地址 \| 函数名`，用于在 93 MB 文本里直接定位 |
| `INDEX.md` | 七个插件反编译产物的总索引（原 `decomp_full/INDEX.md`） |

反编译源码用途：查真实实现，例如 `EncryptionLock::getProtectionTimeout`、`WCREncryptionBiometricInProgress`、TTS 采样率常量 `DAT_00003e80 = 16000` 等，之前已用它交叉验证过踏浪插件的防撤回线程问题和 16 kHz 采样率修复。

## 03_分析文档

| 文件 | 说明 |
| --- | --- |
| `WCRefine_安全自评.md` | 授权 / 口令 / 完整性保护的安全自评（含明文口令、25 个硬编码 SHA256、服务端校验地址等发现） |
| `分析报告.md` | 7 个 rootless 微信 tweak 的静态结构、符号、字符串、依赖、加密特征分析 |
| `analysis_report.json` | 689 KB 机器可读分析数据 |
| `MachO分析方案说明.md` | Windows 上跑 Mach-O / Ghidra headless 的方法与踩坑记录 |

## 04_原始二进制与分析脚本

| 文件 | 说明 |
| --- | --- |
| `WCRefine.dylib` | 45.2 MB arm64 Mach-O，从 deb 解出 |
| `analyze_macho.py` | 自写 Mach-O / ObjC 字符串解析器（Windows 下无需 macOS 工具） |
| `extract_highlights.py` | 亮点抽取脚本 |

---

## 边界说明

- 全部内容来自你本人提供的样本，仅做**静态结构分析与函数级反编译**，不含任何运行时修改、授权绕过、鉴权跳过工具或方法。
- `WCRefine_安全自评.md` 指出其防护弱点属于安全评估结论，不提供利用手段。
- 反编译 C 是 Ghidra 生成的伪代码，不是作者原始 Objective-C 源码，变量名为还原命名，逻辑需结合符号表判断。
- 第三方插件有授权 / 完整性校验，安装使用请遵守对应许可；本包仅作本地研究资料留存。
