# iOS 应用结构体检报告

- 生成时间：2026-11-10T11:54:09.904953+08:00
- 输入文件：`E:\iOS-App-Analysis\01-IPA\Soul_6.41.0.ipa`
- 文件大小：209.94 MiB
- SHA-256：`84497208f44b7cc459eeede5ef93b2339690bf5e61773a949e5b24f47878f4f0`

## 应用元数据

| 字段 | 值 |
| --- | --- |
| `CFBundleIdentifier` | com.soulapp.cn |
| `CFBundleExecutable` | Soul_New |
| `CFBundleShortVersionString` | 6.41.0 |
| `CFBundleVersion` | 261029205000 |
| `MinimumOSVersion` | 15.0 |
| `CFBundleSupportedPlatforms` | ['iPhoneOS'] |
| `UIDeviceFamily` | [1, 2] |
| `NSAppTransportSecurity` | {'NSAllowsArbitraryLoads': True, 'NSExceptionDomains': {'sinaimg.cn': {'NSThirdPartyExceptionAllowsInsecureHTTPLoads': True, 'NSThirdPartyExceptionRequiresForwa ... |
| `CFBundleURLTypes` | [{'CFBundleTypeRole': 'Editor', 'CFBundleURLName': 'wechat', 'CFBundleURLSchemes': ['wxcc5f58957efdffe9']}, {'CFBundleTypeRole': 'Editor', 'CFBundleURLSchemes': ... |
| `UISupportedInterfaceOrientations` | ['UIInterfaceOrientationPortrait'] |
| `ITSAppUsesNonExemptEncryption` | False |
| `NSCameraUsageDescription` | 为了您能正常体验拍照、录制视频/表情包、视频匹配、扫一扫等功能，Soul需要申请相机权限。如您拒绝授权，不影响您使用APP的其他功能。 |
| `NSPhotoLibraryUsageDescription` | 为了您能正常分享图片/视频、保存图片/视频，Soul需要申请存储权限。如您拒绝授权，不影响您使用APP的其他功能。 |
| `NSMicrophoneUsageDescription` | 为了您能正常体验语音输入、语音变声、语音匹配、视频匹配等功能，Soul需要申请麦克风权限。如您拒绝授权，不影响您使用APP的其他功能。 |
| `NSLocationWhenInUseUsageDescription` | 为了您能正常体验以下功能：奇遇铃、发帖时展示地理位置、查看您和附近用户的大致距离、匹配附近的用户或瞬间等；Soul需申请获取您的位置权限。如您拒绝授权，则您无法正常使用上述功能，但不影响您使用APP的其他功能。 |
| `executable` | Payload/Soul_New.app/Soul_New |
| `executable_size` | 217173488 |

## 包内容概览

- 条目总数：4094
- 内嵌 framework：39 个
- 动态库/framework 路径：39 条
- 含描述文件：否
- 含代码签名目录：是
- 含隐私清单 PrivacyInfo.xcprivacy：是

### 内嵌 framework（前 30）

- `AdjustSigSdk.framework`
- `AgoraAudioBeautyExtension.framework`
- `AgoraRtcKit.framework`
- `AgoraSoundTouch.framework`
- `Agorafdkaac.framework`
- `Agoraffmpeg.framework`
- `ByteRTCFFmpegAudioExtension.framework`
- `CFGameSDK.framework`
- `GDTMobSDK.framework`
- `GTNetwork.framework`
- `OpenSSL.framework`
- `RTCFFmpeg.framework`
- `RealXBase.framework`
- `SLFFmpeg.framework`
- `TECodec.framework`
- `TTFFmpeg.framework`
- `TTSDKCore.framework`
- `TTSDKPlayer.framework`
- `TTSDKPlayerCoreNormal.framework`
- `TTSDKReachability.framework`
- `TTSDKTTFFmpegNormal.framework`
- `TTSDKTools.framework`
- `TTSDKTopSignature.framework`
- `TTSDKVCN.framework`
- `TTSDKVolcLog.framework`
- `TTVideoEditor.framework`
- `TXFFmpeg.framework`
- `TXSoundTouch.framework`
- `Tquic.framework`
- `VolcBaseLog.framework`

### 文件类型分布（前 12）

| 扩展名 | 数量 |
| --- | ---: |
| `.h` | 1334 |
| `.png` | 1040 |
| `(no ext)` | 353 |
| `.json` | 335 |
| `.hpp` | 194 |
| `.zip` | 154 |
| `.plist` | 153 |
| `.svg` | 126 |
| `.css` | 90 |
| `.strings` | 60 |
| `.sz` | 57 |
| `.mp3` | 40 |

## Mach-O 结构（容器：thin）

### 切片 single

- 类型：MH_EXECUTE / CPU：ARM64 / 子类型：0x00000000
- 加载命令：175 条，共 17744 字节
- 编译标志：MH_NOUNDEFS, MH_DYLDLINK, MH_TWOLEVEL, MH_WEAK_DEFINES, MH_BINDS_TO_WEAK, MH_PIE, MH_HAS_TLV_DESCRIPTORS
- UUID：D88E6E6C754B3C7EBC80F6F879AD3C12
- 构建版本：{'platform': 2, 'minos': '15.0.0', 'sdk': '27.1.0', 'ntools': 1}
- 加密状态：not encrypted
- 代码签名：有
- 依赖 dylib：154 个 / rpath：3 条

| 段 | VM 大小 | 文件偏移 | 节数 |
| --- | ---: | ---: | ---: |
| `__PAGEZERO` | 4294967296 | 0 | 0 |
| `__TEXT` | 169902080 | 0 | 31 |
| `__DATA_CONST` | 7454720 | 169902080 | 15 |
| `__DATA` | 31293440 | 177356800 | 20 |
| `__LINKEDIT` | 12009472 | 205176832 | 0 |

<details><summary>依赖库清单</summary>

- `/usr/lib/libbz2.1.0.dylib` （LC_LOAD_DYLIB）
- `/usr/lib/libSystem.B.dylib` （LC_LOAD_DYLIB）
- `/usr/lib/libc++.1.dylib` （LC_LOAD_DYLIB）
- `/usr/lib/libc++abi.dylib` （LC_LOAD_DYLIB）
- `/usr/lib/libcompression.dylib` （LC_LOAD_DYLIB）
- `/usr/lib/libiconv.2.dylib` （LC_LOAD_DYLIB）
- `/usr/lib/libresolv.9.dylib` （LC_LOAD_DYLIB）
- `/usr/lib/libsqlite3.dylib` （LC_LOAD_DYLIB）
- `/usr/lib/libxml2.2.dylib` （LC_LOAD_DYLIB）
- `/usr/lib/libz.1.dylib` （LC_LOAD_DYLIB）
- `/System/Library/Frameworks/AVFoundation.framework/AVFoundation` （LC_LOAD_WEAK_DYLIB）
- `/System/Library/Frameworks/AVKit.framework/AVKit` （LC_LOAD_DYLIB）
- `/System/Library/Frameworks/Accelerate.framework/Accelerate` （LC_LOAD_DYLIB）
- `/System/Library/Frameworks/AdSupport.framework/AdSupport` （LC_LOAD_WEAK_DYLIB）
- `/System/Library/Frameworks/AddressBook.framework/AddressBook` （LC_LOAD_DYLIB）
- `@rpath/AdjustSigSdk.framework/AdjustSigSdk` （LC_LOAD_DYLIB）
- `@rpath/AgoraAudioBeautyExtension.framework/AgoraAudioBeautyExtension` （LC_LOAD_WEAK_DYLIB）
- `@rpath/AgoraRtcKit.framework/AgoraRtcKit` （LC_LOAD_DYLIB）
- `@rpath/AgoraSoundTouch.framework/AgoraSoundTouch` （LC_LOAD_DYLIB）
- `@rpath/Agorafdkaac.framework/Agorafdkaac` （LC_LOAD_DYLIB）
- `@rpath/Agoraffmpeg.framework/Agoraffmpeg` （LC_LOAD_DYLIB）
- `/System/Library/Frameworks/AssetsLibrary.framework/AssetsLibrary` （LC_LOAD_DYLIB）
- `/System/Library/Frameworks/AudioToolbox.framework/AudioToolbox` （LC_LOAD_DYLIB）
- `@rpath/ByteRTCFFmpegAudioExtension.framework/ByteRTCFFmpegAudioExtension` （LC_LOAD_DYLIB）
- `@rpath/CFGameSDK.framework/CFGameSDK` （LC_LOAD_DYLIB）
- `/System/Library/Frameworks/CFNetwork.framework/CFNetwork` （LC_LOAD_DYLIB）
- `/System/Library/Frameworks/CoreAudio.framework/CoreAudio` （LC_LOAD_DYLIB）
- `/System/Library/Frameworks/CoreFoundation.framework/CoreFoundation` （LC_LOAD_WEAK_DYLIB）
- `/System/Library/Frameworks/CoreGraphics.framework/CoreGraphics` （LC_LOAD_DYLIB）
- `/System/Library/Frameworks/CoreHaptics.framework/CoreHaptics` （LC_LOAD_WEAK_DYLIB）
- `/System/Library/Frameworks/CoreImage.framework/CoreImage` （LC_LOAD_DYLIB）
- `/System/Library/Frameworks/CoreLocation.framework/CoreLocation` （LC_LOAD_DYLIB）
- `/System/Library/Frameworks/CoreML.framework/CoreML` （LC_LOAD_WEAK_DYLIB）
- `/System/Library/Frameworks/CoreMedia.framework/CoreMedia` （LC_LOAD_WEAK_DYLIB）
- `/System/Library/Frameworks/CoreMotion.framework/CoreMotion` （LC_LOAD_WEAK_DYLIB）
- `/System/Library/Frameworks/CoreServices.framework/CoreServices` （LC_LOAD_DYLIB）
- `/System/Library/Frameworks/CoreTelephony.framework/CoreTelephony` （LC_LOAD_WEAK_DYLIB）
- `/System/Library/Frameworks/CoreText.framework/CoreText` （LC_LOAD_DYLIB）
- `/System/Library/Frameworks/CoreVideo.framework/CoreVideo` （LC_LOAD_DYLIB）
- `/System/Library/Frameworks/DeviceCheck.framework/DeviceCheck` （LC_LOAD_WEAK_DYLIB）
- `/System/Library/Frameworks/EventKit.framework/EventKit` （LC_LOAD_DYLIB）
- `/System/Library/Frameworks/Foundation.framework/Foundation` （LC_LOAD_DYLIB）
- `@rpath/GDTMobSDK.framework/GDTMobSDK` （LC_LOAD_DYLIB）
- `/System/Library/Frameworks/GLKit.framework/GLKit` （LC_LOAD_DYLIB）
- `@rpath/GTNetwork.framework/GTNetwork` （LC_LOAD_DYLIB）
- `/System/Library/Frameworks/IOKit.framework/Versions/A/IOKit` （LC_LOAD_DYLIB）
- `/System/Library/Frameworks/ImageIO.framework/ImageIO` （LC_LOAD_DYLIB）
- `/System/Library/Frameworks/JavaScriptCore.framework/JavaScriptCore` （LC_LOAD_DYLIB）
- `/System/Library/Frameworks/LocalAuthentication.framework/LocalAuthentication` （LC_LOAD_DYLIB）
- `/System/Library/Frameworks/MapKit.framework/MapKit` （LC_LOAD_DYLIB）
- `/System/Library/Frameworks/MediaPlayer.framework/MediaPlayer` （LC_LOAD_DYLIB）
- `/System/Library/Frameworks/MediaToolbox.framework/MediaToolbox` （LC_LOAD_DYLIB）
- `/System/Library/Frameworks/Metal.framework/Metal` （LC_LOAD_WEAK_DYLIB）
- `/System/Library/Frameworks/MetalKit.framework/MetalKit` （LC_LOAD_WEAK_DYLIB）
- `/System/Library/Frameworks/MetalPerformanceShaders.framework/MetalPerformanceShaders` （LC_LOAD_WEAK_DYLIB）
- `/System/Library/Frameworks/MobileCoreServices.framework/MobileCoreServices` （LC_LOAD_DYLIB）
- `/System/Library/Frameworks/OpenAL.framework/OpenAL` （LC_LOAD_WEAK_DYLIB）
- `/System/Library/Frameworks/OpenGLES.framework/OpenGLES` （LC_LOAD_DYLIB）
- `@rpath/OpenSSL.framework/OpenSSL` （LC_LOAD_DYLIB）
- `/System/Library/Frameworks/Photos.framework/Photos` （LC_LOAD_DYLIB）
- `/System/Library/Frameworks/QuartzCore.framework/QuartzCore` （LC_LOAD_DYLIB）
- `@rpath/RTCFFmpeg.framework/RTCFFmpeg` （LC_LOAD_DYLIB）
- `@rpath/RealXBase.framework/RealXBase` （LC_LOAD_DYLIB）
- `@rpath/SLFFmpeg.framework/SLFFmpeg` （LC_LOAD_DYLIB）
- `/System/Library/Frameworks/SafariServices.framework/SafariServices` （LC_LOAD_DYLIB）
- `/System/Library/Frameworks/Security.framework/Security` （LC_LOAD_DYLIB）
- `/System/Library/Frameworks/StoreKit.framework/StoreKit` （LC_LOAD_DYLIB）
- `/System/Library/Frameworks/SystemConfiguration.framework/SystemConfiguration` （LC_LOAD_WEAK_DYLIB）
- `@rpath/TECodec.framework/TECodec` （LC_LOAD_DYLIB）
- `@rpath/TTFFmpeg.framework/TTFFmpeg` （LC_LOAD_DYLIB）
- `@rpath/TTSDKCore.framework/TTSDKCore` （LC_LOAD_DYLIB）
- `@rpath/TTSDKPlayer.framework/TTSDKPlayer` （LC_LOAD_DYLIB）
- `@rpath/TTSDKPlayerCoreNormal.framework/TTSDKPlayerCoreNormal` （LC_LOAD_DYLIB）
- `@rpath/TTSDKReachability.framework/TTSDKReachability` （LC_LOAD_DYLIB）
- `@rpath/TTSDKTTFFmpegNormal.framework/TTSDKTTFFmpegNormal` （LC_LOAD_DYLIB）
- `@rpath/TTSDKTools.framework/TTSDKTools` （LC_LOAD_DYLIB）
- `@rpath/TTSDKTopSignature.framework/TTSDKTopSignature` （LC_LOAD_DYLIB）
- `@rpath/TTSDKVCN.framework/TTSDKVCN` （LC_LOAD_DYLIB）
- `@rpath/TTSDKVolcLog.framework/TTSDKVolcLog` （LC_LOAD_DYLIB）
- `@rpath/TXFFmpeg.framework/TXFFmpeg` （LC_LOAD_DYLIB）
- `@rpath/TXSoundTouch.framework/TXSoundTouch` （LC_LOAD_DYLIB）
- `@rpath/Tquic.framework/Tquic` （LC_LOAD_DYLIB）
- `/System/Library/Frameworks/UIKit.framework/UIKit` （LC_LOAD_DYLIB）
- `/System/Library/Frameworks/VideoToolbox.framework/VideoToolbox` （LC_LOAD_DYLIB）
- `@rpath/VolcBaseLog.framework/VolcBaseLog` （LC_LOAD_DYLIB）
- `@rpath/VolcEngineRTC.framework/VolcEngineRTC` （LC_LOAD_DYLIB）
- `/System/Library/Frameworks/WebKit.framework/WebKit` （LC_LOAD_WEAK_DYLIB）
- `@rpath/XMagic.framework/XMagic` （LC_LOAD_DYLIB）
- `@rpath/YTCommonXMagic.framework/YTCommonXMagic` （LC_LOAD_DYLIB）
- `@rpath/bytenn.framework/bytenn` （LC_LOAD_DYLIB）
- `@rpath/hermes.framework/hermes` （LC_LOAD_DYLIB）
- `@rpath/libpag.framework/libpag` （LC_LOAD_DYLIB）
- `@rpath/libvcn.framework/libvcn` （LC_LOAD_DYLIB）
- `@rpath/ttboringssl.framework/ttboringssl` （LC_LOAD_DYLIB）
- `@rpath/ttcrypto.framework/ttcrypto` （LC_LOAD_DYLIB）
- `/System/Library/Frameworks/ARKit.framework/ARKit` （LC_LOAD_WEAK_DYLIB）
- `/System/Library/Frameworks/AppTrackingTransparency.framework/AppTrackingTransparency` （LC_LOAD_WEAK_DYLIB）
- `/System/Library/Frameworks/MetricKit.framework/MetricKit` （LC_LOAD_WEAK_DYLIB）
- `@rpath/TTVideoEditor.framework/TTVideoEditor` （LC_LOAD_DYLIB）
- `/System/Library/Frameworks/UserNotifications.framework/UserNotifications` （LC_LOAD_WEAK_DYLIB）
- `/System/Library/Frameworks/SwiftUI.framework/SwiftUI` （LC_LOAD_WEAK_DYLIB）
- `/System/Library/Frameworks/ReplayKit.framework/ReplayKit` （LC_LOAD_DYLIB）
- `/System/Library/Frameworks/AuthenticationServices.framework/AuthenticationServices` （LC_LOAD_DYLIB）
- `/System/Library/Frameworks/BackgroundTasks.framework/BackgroundTasks` （LC_LOAD_WEAK_DYLIB）
- `/System/Library/Frameworks/ActivityKit.framework/ActivityKit` （LC_LOAD_WEAK_DYLIB）
- `/System/Library/Frameworks/AdServices.framework/AdServices` （LC_LOAD_WEAK_DYLIB）
- `/System/Library/Frameworks/SceneKit.framework/SceneKit` （LC_LOAD_DYLIB）
- `/usr/lib/libicucore.A.dylib` （LC_LOAD_DYLIB）
- `/usr/lib/libobjc.A.dylib` （LC_LOAD_DYLIB）
- `/System/Library/Frameworks/AVFAudio.framework/AVFAudio` （LC_LOAD_WEAK_DYLIB）
- `/System/Library/Frameworks/Accounts.framework/Accounts` （LC_LOAD_DYLIB）
- `/System/Library/Frameworks/Combine.framework/Combine` （LC_LOAD_DYLIB）
- `/System/Library/Frameworks/Contacts.framework/Contacts` （LC_LOAD_DYLIB）
- `/System/Library/Frameworks/CoreBluetooth.framework/CoreBluetooth` （LC_LOAD_DYLIB）
- `/System/Library/Frameworks/CoreSpotlight.framework/CoreSpotlight` （LC_LOAD_DYLIB）
- `/System/Library/Frameworks/Intents.framework/Intents` （LC_LOAD_DYLIB）
- `/System/Library/Frameworks/Network.framework/Network` （LC_LOAD_DYLIB）
- `/System/Library/Frameworks/PhotosUI.framework/PhotosUI` （LC_LOAD_DYLIB）
- `/System/Library/Frameworks/WidgetKit.framework/WidgetKit` （LC_LOAD_DYLIB）
- `/usr/lib/swift/libswiftAVFoundation.dylib` （LC_LOAD_WEAK_DYLIB）
- `/usr/lib/swift/libswiftAccelerate.dylib` （LC_LOAD_WEAK_DYLIB）
- `/usr/lib/swift/libswiftCompression.dylib` （LC_LOAD_WEAK_DYLIB）
- `/usr/lib/swift/libswiftCore.dylib` （LC_LOAD_DYLIB）
- `/usr/lib/swift/libswiftCoreAudio.dylib` （LC_LOAD_WEAK_DYLIB）
- `/usr/lib/swift/libswiftCoreFoundation.dylib` （LC_LOAD_DYLIB）
- `/usr/lib/swift/libswiftCoreImage.dylib` （LC_LOAD_WEAK_DYLIB）
- `/usr/lib/swift/libswiftCoreLocation.dylib` （LC_LOAD_WEAK_DYLIB）
- `/usr/lib/swift/libswiftCoreMIDI.dylib` （LC_LOAD_WEAK_DYLIB）
- `/usr/lib/swift/libswiftDarwin.dylib` （LC_LOAD_DYLIB）
- `/usr/lib/swift/libswiftDataDetection.dylib` （LC_LOAD_WEAK_DYLIB）
- `/usr/lib/swift/libswiftDispatch.dylib` （LC_LOAD_DYLIB）
- `/usr/lib/swift/libswiftGLKit.dylib` （LC_LOAD_WEAK_DYLIB）
- `/usr/lib/swift/libswiftIntents.dylib` （LC_LOAD_WEAK_DYLIB）
- `/usr/lib/swift/libswiftMapKit.dylib` （LC_LOAD_WEAK_DYLIB）
- `/usr/lib/swift/libswiftMetal.dylib` （LC_LOAD_WEAK_DYLIB）
- `/usr/lib/swift/libswiftMetalKit.dylib` （LC_LOAD_WEAK_DYLIB）
- `/usr/lib/swift/libswiftModelIO.dylib` （LC_LOAD_WEAK_DYLIB）
- `/usr/lib/swift/libswiftOSLog.dylib` （LC_LOAD_WEAK_DYLIB）
- `/usr/lib/swift/libswiftObjectiveC.dylib` （LC_LOAD_DYLIB）
- `/usr/lib/swift/libswiftQuartzCore.dylib` （LC_LOAD_DYLIB）
- `/usr/lib/swift/libswiftSpatial.dylib` （LC_LOAD_WEAK_DYLIB）
- `/usr/lib/swift/libswiftUniformTypeIdentifiers.dylib` （LC_LOAD_WEAK_DYLIB）
- `/usr/lib/swift/libswiftXPC.dylib` （LC_LOAD_WEAK_DYLIB）
- `/usr/lib/swift/libswift_Concurrency.dylib` （LC_LOAD_DYLIB）
- `/usr/lib/swift/libswiftos.dylib` （LC_LOAD_WEAK_DYLIB）
- `/usr/lib/swift/libswiftsimd.dylib` （LC_LOAD_WEAK_DYLIB）
- `/usr/lib/swift/libswiftCoreGraphics.dylib` （LC_LOAD_DYLIB）
- `/usr/lib/swift/libswiftCoreMedia.dylib` （LC_LOAD_DYLIB）
- `/usr/lib/swift/libswiftFoundation.dylib` （LC_LOAD_DYLIB）
- `/usr/lib/swift/libswiftPhotos.dylib` （LC_LOAD_DYLIB）
- `/usr/lib/swift/libswiftWebKit.dylib` （LC_LOAD_WEAK_DYLIB）
- `/usr/lib/swift/libswiftUIKit.dylib` （LC_LOAD_DYLIB）
- `/usr/lib/swift/libswiftFileProvider.dylib` （LC_LOAD_WEAK_DYLIB）
- `/usr/lib/swift/libswiftPhotosUI.dylib` （LC_LOAD_DYLIB）

</details>

**防护/运行时检测字符串观察**（仅统计字面量出现次数，不做绕过推断）

| 关键字 | 出现次数 |
| --- | ---: |
| `NSURLSession` | 260 |
| `CFNetwork` | 18 |
| `Substrate` | 15 |
| `sysctl` | 15 |
| `ATS` | 15 |
| `MobileSubstrate` | 12 |
| `jailbreak` | 10 |
| `Jailbreak` | 8 |
| `cydia` | 8 |
| `SecTrustEvaluate` | 8 |
| `SSLSetSessionOption` | 6 |
| `objc_msgSend` | 6 |
| `jailbroken` | 2 |
| `posix_spawn` | 2 |
| `os_proc` | 2 |
| `DYLD_INSERT_LIBRARIES` | 1 |
| `Frida` | 1 |
| `frida` | 1 |
| `ptrace` | 1 |
| `amfid` | 1 |
| `/Applications/Cydia.app` | 1 |

---

本报告只记录文件结构与公开元数据，用于学习 iOS 二进制组织方式与安全加固现状；
不包含、也不构成对任何技术措施的规避方法。
