# iOS 应用结构体检报告

- 生成时间：2026-11-09T00:27:05.039649+08:00
- 输入文件：`E:\iOS-App-Analysis\02-Extracted\pipeline-sample.ipa`
- 文件大小：9.97 MiB
- SHA-256：`1ff46084347e06ab9ffec18f6d15065baa9d966ea7efac7cb0a1e5fa77817bc6`

## 应用元数据

| 字段 | 值 |
| --- | --- |
| `CFBundleIdentifier` | com.dumpapp.ath |
| `CFBundleExecutable` | DumpApp |
| `CFBundleShortVersionString` | 1.3.1 |
| `CFBundleVersion` | 1 |
| `MinimumOSVersion` | 12.0 |
| `CFBundleSupportedPlatforms` | ['iPhoneOS'] |
| `UIDeviceFamily` | [1, 2] |
| `NSAppTransportSecurity` | {'NSAllowsArbitraryLoads': True} |
| `CFBundleURLTypes` | [{'CFBundleTypeRole': 'Editor', 'CFBundleURLIconFile': '', 'CFBundleURLSchemes': ['dumpath']}] |
| `UISupportedInterfaceOrientations` | ['UIInterfaceOrientationPortrait', 'UIInterfaceOrientationPortraitUpsideDown'] |
| `NSCameraUsageDescription` | 使用相机权限 |
| `NSPhotoLibraryUsageDescription` | 需要打开相册权限，访问相册选择照片 |
| `executable` | Payload/DumpApp.app/DumpApp |
| `executable_size` | 28098336 |

## 包内容概览

- 条目总数：113
- 内嵌 framework：1 个
- 动态库/framework 路径：3 条
- 含描述文件：是
- 含代码签名目录：是
- 含隐私清单 PrivacyInfo.xcprivacy：是

### 内嵌 framework（前 30）

- `FlutterOS.framework`

### 文件类型分布（前 12）

| 扩展名 | 数量 |
| --- | ---: |
| `.png` | 34 |
| `(no ext)` | 30 |
| `.nib` | 12 |
| `.plist` | 8 |
| `.strings` | 7 |
| `.json` | 4 |
| `.mobileprovision` | 2 |
| `.dylib` | 2 |
| `.car` | 2 |
| `.ds_store` | 1 |
| `.p12` | 1 |
| `.inc` | 1 |

## Mach-O 结构（容器：thin）

### 切片 single

- 类型：MH_EXECUTE / CPU：ARM64 / 子类型：0x00000000
- 加载命令：72 条，共 8408 字节
- 编译标志：MH_NOUNDEFS, MH_DYLDLINK, MH_TWOLEVEL, MH_WEAK_DEFINES, MH_BINDS_TO_WEAK, MH_PIE
- UUID：670790EEB0163EAE8940C04E748E4D56
- 构建版本：{'platform': 2, 'minos': '12.0.0', 'sdk': '17.4.0', 'ntools': 1}
- 加密状态：not encrypted
- 代码签名：有
- 依赖 dylib：54 个 / rpath：2 条

| 段 | VM 大小 | 文件偏移 | 节数 |
| --- | ---: | ---: | ---: |
| `__PAGEZERO` | 4294967296 | 0 | 0 |
| `__TEXT` | 13451264 | 0 | 21 |
| `__DATA` | 2637824 | 13451264 | 25 |
| `__LINKEDIT` | 12107776 | 15990784 | 0 |

<details><summary>依赖库清单</summary>

- `/usr/lib/libc++.1.dylib` （LC_LOAD_DYLIB）
- `/usr/lib/libsqlite3.dylib` （LC_LOAD_DYLIB）
- `/usr/lib/libxml2.2.dylib` （LC_LOAD_DYLIB）
- `/usr/lib/libz.1.dylib` （LC_LOAD_DYLIB）
- `/System/Library/Frameworks/AVFoundation.framework/AVFoundation` （LC_LOAD_DYLIB）
- `/System/Library/Frameworks/Accelerate.framework/Accelerate` （LC_LOAD_DYLIB）
- `/System/Library/Frameworks/AssetsLibrary.framework/AssetsLibrary` （LC_LOAD_DYLIB）
- `/System/Library/Frameworks/CFNetwork.framework/CFNetwork` （LC_LOAD_DYLIB）
- `/System/Library/Frameworks/CoreFoundation.framework/CoreFoundation` （LC_LOAD_DYLIB）
- `/System/Library/Frameworks/CoreGraphics.framework/CoreGraphics` （LC_LOAD_DYLIB）
- `/System/Library/Frameworks/CoreImage.framework/CoreImage` （LC_LOAD_DYLIB）
- `/System/Library/Frameworks/CoreMedia.framework/CoreMedia` （LC_LOAD_DYLIB）
- `/System/Library/Frameworks/CoreMotion.framework/CoreMotion` （LC_LOAD_DYLIB）
- `/System/Library/Frameworks/CoreServices.framework/CoreServices` （LC_LOAD_DYLIB）
- `/System/Library/Frameworks/CoreTelephony.framework/CoreTelephony` （LC_LOAD_DYLIB）
- `/System/Library/Frameworks/CoreText.framework/CoreText` （LC_LOAD_DYLIB）
- `/System/Library/Frameworks/Foundation.framework/Foundation` （LC_LOAD_DYLIB）
- `/System/Library/Frameworks/ImageIO.framework/ImageIO` （LC_LOAD_DYLIB）
- `/System/Library/Frameworks/MobileCoreServices.framework/MobileCoreServices` （LC_LOAD_DYLIB）
- `/System/Library/Frameworks/Photos.framework/Photos` （LC_LOAD_DYLIB）
- `/System/Library/Frameworks/PhotosUI.framework/PhotosUI` （LC_LOAD_DYLIB）
- `/System/Library/Frameworks/QuartzCore.framework/QuartzCore` （LC_LOAD_DYLIB）
- `/System/Library/Frameworks/Security.framework/Security` （LC_LOAD_DYLIB）
- `/System/Library/Frameworks/SystemConfiguration.framework/SystemConfiguration` （LC_LOAD_DYLIB）
- `/System/Library/Frameworks/UIKit.framework/UIKit` （LC_LOAD_DYLIB）
- `/System/Library/Frameworks/WebKit.framework/WebKit` （LC_LOAD_DYLIB）
- `/usr/lib/libarchive.2.dylib` （LC_LOAD_DYLIB）
- `/usr/lib/libiconv.2.dylib` （LC_LOAD_DYLIB）
- `/System/Library/Frameworks/SafariServices.framework/SafariServices` （LC_LOAD_DYLIB）
- `/usr/lib/libobjc.A.dylib` （LC_LOAD_DYLIB）
- `/usr/lib/libSystem.B.dylib` （LC_LOAD_DYLIB）
- `/System/Library/Frameworks/AdSupport.framework/AdSupport` （LC_LOAD_DYLIB）
- `/System/Library/Frameworks/AppTrackingTransparency.framework/AppTrackingTransparency` （LC_LOAD_WEAK_DYLIB）
- `/System/Library/Frameworks/AudioToolbox.framework/AudioToolbox` （LC_LOAD_DYLIB）
- `/System/Library/Frameworks/CoreData.framework/CoreData` （LC_LOAD_DYLIB）
- `/System/Library/Frameworks/MapKit.framework/MapKit` （LC_LOAD_DYLIB）
- `/System/Library/Frameworks/SwiftUI.framework/SwiftUI` （LC_LOAD_WEAK_DYLIB）
- `/usr/lib/swift/libswiftDataDetection.dylib` （LC_LOAD_WEAK_DYLIB）
- `/usr/lib/swift/libswiftFileProvider.dylib` （LC_LOAD_WEAK_DYLIB）
- `/usr/lib/swift/libswiftOSLog.dylib` （LC_LOAD_WEAK_DYLIB）
- `/usr/lib/swift/libswiftUniformTypeIdentifiers.dylib` （LC_LOAD_WEAK_DYLIB）
- `@rpath/libswiftCore.dylib` （LC_LOAD_DYLIB）
- `@rpath/libswiftCoreFoundation.dylib` （LC_LOAD_WEAK_DYLIB）
- `@rpath/libswiftCoreImage.dylib` （LC_LOAD_WEAK_DYLIB）
- `@rpath/libswiftDarwin.dylib` （LC_LOAD_WEAK_DYLIB）
- `@rpath/libswiftDispatch.dylib` （LC_LOAD_DYLIB）
- `@rpath/libswiftMetal.dylib` （LC_LOAD_WEAK_DYLIB）
- `@rpath/libswiftObjectiveC.dylib` （LC_LOAD_DYLIB）
- `@rpath/libswiftQuartzCore.dylib` （LC_LOAD_WEAK_DYLIB）
- `@rpath/libswiftXPC.dylib` （LC_LOAD_WEAK_DYLIB）
- `@rpath/libswiftos.dylib` （LC_LOAD_WEAK_DYLIB）
- `@rpath/libswiftCoreGraphics.dylib` （LC_LOAD_WEAK_DYLIB）
- `@rpath/libswiftFoundation.dylib` （LC_LOAD_DYLIB）
- `@rpath/libswiftUIKit.dylib` （LC_LOAD_WEAK_DYLIB）

</details>

**防护/运行时检测字符串观察**（仅统计字面量出现次数，不做绕过推断）

| 关键字 | 出现次数 |
| --- | ---: |
| `objc_msgSend` | 11593 |
| `NSURLSession` | 230 |
| `sysctl` | 32 |
| `Substrate` | 10 |
| `jailbroken` | 9 |
| `CFNetwork` | 9 |
| `SSLSetSessionOption` | 5 |
| `ATS` | 5 |
| `MobileSubstrate` | 3 |
| `Frida` | 3 |
| `Jailbreak` | 3 |
| `SecTrustEvaluate` | 2 |
| `os_proc` | 2 |
| `/Applications/Cydia.app` | 1 |
| `cydia` | 1 |

---

本报告只记录文件结构与公开元数据，用于学习 iOS 二进制组织方式与安全加固现状；
不包含、也不构成对任何技术措施的规避方法。
