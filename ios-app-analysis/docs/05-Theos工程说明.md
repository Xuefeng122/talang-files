# ResearchKit — Logos / Theos 工程骨架

一个**纯本地界面**的教学模板。它只做三件事：按白名单在宿主界面上挂一个可关闭的面板、读写两个本地开关、输出调试日志。

## 合规声明

- 不 hook 任何第三方业务类；唯一的 `%hook` 目标是系统类 `UIViewController`
- 不改写任何方法返回值，不读取或转发任何用户内容
- 不触碰消息、媒体、支付、广告、水印或会员相关路径
- 过滤 plist 里默认是占位 Bundle ID `com.example.myowndemo`，**默认不注入任何真实应用**
- 只应在你自己编写、或已获得明确授权可测试的应用里启用

## 文件

| 文件 | 作用 |
| --- | --- |
| `Makefile` | 标准 tweak 工程配置，SDK 16.5 / 部署目标 16.0 / arm64 + arm64e |
| `control` | 包元数据 |
| `ResearchKit.plist` | 注入过滤（占位 Bundle ID） |
| `Tweak.x` | Logos 钩子：`%hook` / `%new` / `%property` / `%group` / `%ctor` / `%init` |
| `RKPanel.h` / `RKPanel.m` | 纯 UIKit 菜单面板：宿主信息、两个开关、关闭按钮、用途说明 |
| `RKSettings.h` / `RKSettings.m` | 本地偏好读写与白名单判断 |

## 菜单面板包含

- 标题（可配置 `PanelTitle`）
- 宿主 Bundle ID、版本号、系统版本、面板版本 — 只读展示
- `Enable panel` 总开关（默认关闭）
- `Debug logging` 日志开关（默认关闭）
- 关闭按钮与一段英文用途说明
- 毛玻璃背景、圆角、淡入淡出

## 启用方式

把 `ResearchKit.plist` 与偏好里的 `AllowedBundleIdentifiers` 改成**你自己有权限测试的应用**的 Bundle ID，然后把 `Enabled` 设为 `YES`。两个地方都通过才会安装钩子并显示面板。

偏好字典结构（键 `ResearchKitPrefs`）：

```
Enabled                    = YES / NO
Logging                    = YES / NO
PanelTitle                 = "My Panel"
AllowedBundleIdentifiers   = [ "com.yourcompany.yourdemo" ]
```

也可以把同样的字典放进宿主 App 的 `Info.plist`，键名 `ResearchKitDefaults`，作为首次运行的默认值。

## Logos 规范要点（本工程已遵循）

1. 默认用 `.x`；只有用到 `MSHookIvar` / C++ 的那一个文件才改 `.xm`
2. 新增方法写 `%new(typeencoding)`，例如 `%new(v@:@)` 对应 `- (void)foo:(id)sender`
3. `%orig` / `%orig(arg)` 不传 `self`、`_cmd`；`%new` 方法里不能调 `%orig`
4. 分组钩子必须在 `%ctor` 里显式 `%init(GroupName)`，不会自动初始化
5. 消息发送一律用 `[receiver message]`；私有选择器先补 `@interface` 声明，不用 `objc_msgSend`
6. tweak 自己加的状态用 `%property`，不手写 `objc_setAssociatedObject`
7. 目标类私有实例变量用 `MSHookIvar<T>`，不手算 `ivar_getOffset`
8. 动态符号用 `MSFindSymbol(MSGetImageByName("/path/to/image"), "_symbol")`，不传 `NULL`
9. 不在 Logos 文件里 `#include <substrate.h>`，Theos 会自动加
10. 每个 `%hook` 单独成块，以 `%end` 收尾；同一组里不要重复 hook 同一方法

## 编译

**本机 Windows 目前编不了**（详见 `03-Analysis/分析报告.md`）：GnuWin32 是原生 make，`uname -s` 取不到平台值，且缺 `ldid` 与 arm64 Mach-O 链接器。

在 macOS / Linux / 配好工具链的 WSL 里：

```bash
export THEOS=/opt/theos          # 换成你的 Theos 路径
cd ResearchKit
make clean
make package                     # 产出 .deb
```

需要的组件：Theos 本体、对应版本的 iPhoneOS SDK、clang、`ldid`、`dpkg-deb`（或 Theos 自带的 dm.pl）、`perl`、`make`、Logos（Theos 自带）、MobileSubstrate/libhooker 头文件。

## 自检清单

- [ ] 过滤 plist 里没有写任何第三方应用的 Bundle ID
- [ ] `%hook` 只作用于系统类
- [ ] 没有任何读取 / 修改业务数据的代码
- [ ] 默认开关为关闭，白名单默认为占位值
- [ ] `make package` 在受支持平台上通过
