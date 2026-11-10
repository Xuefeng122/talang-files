# iOS 应用结构体检报告

- 生成时间：2026-11-10T11:54:05.678617+08:00
- 输入文件：`E:\iOS-App-Analysis\01-IPA\MOMO陌陌_9.23.2.ipa`
- 文件大小：157.55 MiB
- SHA-256：`fe86448b141057ee8ac79bd67ac7a3b79e247af14c87dce8d1f03524a33ae487`

## 应用元数据

| 字段 | 值 |
| --- | --- |
| `CFBundleIdentifier` | com.wemomo.momoappdemo1 |
| `CFBundleExecutable` | MomoChat |
| `CFBundleShortVersionString` | 9.23.2 |
| `CFBundleVersion` | 9.23.2.7 |
| `MinimumOSVersion` | 15.0 |
| `CFBundleSupportedPlatforms` | ['iPhoneOS'] |
| `UIDeviceFamily` | [1] |
| `NSAppTransportSecurity` | {'NSAllowsArbitraryLoads': True} |
| `CFBundleURLTypes` | [{'CFBundleTypeRole': 'Editor', 'CFBundleURLName': 'com.immomo.momo', 'CFBundleURLSchemes': ['momologinauthorize', 'momochatsdk', 'momochs', 'momoSDK', 'wb20415 ... |
| `UISupportedInterfaceOrientations` | ['UIInterfaceOrientationPortrait'] |
| `ITSAppUsesNonExemptEncryption` | False |
| `NSCameraUsageDescription` | 您还没有开启相机权限，开启后才能正常拍摄照片、视频进行发布，或者通过直播实时分享生活。 |
| `NSPhotoLibraryUsageDescription` | 为了您能正常使用编辑头像、发布动态、发送聊天图片/视频等功能，MOMO陌陌需要申请相册权限。 |
| `NSMicrophoneUsageDescription` | 您还没有开启麦克风权限，开启后才能在正常拍摄视频时录制声音，或者直播时分享声音。 |
| `NSLocationWhenInUseUsageDescription` | 您的位置将用来获取所在地的附近信息，帮助您与附近的人更方便地沟通交流 |
| `executable` | Payload/MomoChat.app/MomoChat |
| `executable_size` | 223240448 |

## 包内容概览

- 条目总数：2725
- 内嵌 framework：41 个
- 动态库/framework 路径：41 条
- 含描述文件：否
- 含代码签名目录：是
- 含隐私清单 PrivacyInfo.xcprivacy：是

### 内嵌 framework（前 30）

- `AgoraAiEchoCancellationExtension.framework`
- `AgoraAiNoiseSuppressionExtension.framework`
- `AgoraAudioBeautyExtension.framework`
- `AgoraRtcKit.framework`
- `AgoraSoundTouch.framework`
- `Agorafdkaac.framework`
- `Agoraffmpeg.framework`
- `ByteRTCFFmpegAudioExtension.framework`
- `RTCFFmpeg.framework`
- `RealXBase.framework`
- `SudMGP.framework`
- `TCGSDK.framework`
- `TTFFmpeg.framework`
- `TTSDKBMF.framework`
- `TTSDKCore.framework`
- `TTSDKHttpDNS.framework`
- `TTSDKLiveBase.framework`
- `TTSDKLivePlayerBMF.framework`
- `TTSDKLivePlayerNormal.framework`
- `TTSDKLivePullVolcLog.framework`
- `TTSDKPlayer.framework`
- `TTSDKPlayerCoreNormal.framework`
- `TTSDKQuicCore.framework`
- `TTSDKQuicPull.framework`
- `TTSDKReachability.framework`
- `TTSDKStrategyPull.framework`
- `TTSDKTTFFmpegNormal.framework`
- `TTSDKTools.framework`
- `TTSDKTopSignature.framework`
- `TTSDKVCN.framework`

### 文件类型分布（前 12）

| 扩展名 | 数量 |
| --- | ---: |
| `.png` | 1316 |
| `(no ext)` | 346 |
| `.glsl` | 310 |
| `.mt` | 195 |
| `.plist` | 114 |
| `.svga` | 87 |
| `.nib` | 69 |
| `.json` | 44 |
| `.lua` | 33 |
| `.zip` | 28 |
| `.mp3` | 17 |
| `.xcprivacy` | 17 |

## Mach-O 结构（容器：thin）

### 切片 single

- 类型：MH_EXECUTE / CPU：ARM64 / 子类型：0x00000000
- 加载命令：179 条，共 19424 字节
- 编译标志：MH_NOUNDEFS, MH_DYLDLINK, MH_TWOLEVEL, MH_WEAK_DEFINES, MH_BINDS_TO_WEAK, MH_PIE, MH_HAS_TLV_DESCRIPTORS
- UUID：94F4545CB80F3AA3B61AA403A0FBBC19
- 构建版本：{'platform': 2, 'minos': '15.0.0', 'sdk': '26.2.0', 'ntools': 4}
- 加密状态：not encrypted
- 代码签名：有
- 依赖 dylib：156 个 / rpath：3 条

| 段 | VM 大小 | 文件偏移 | 节数 |
| --- | ---: | ---: | ---: |
| `__PAGEZERO` | 4294967296 | 0 | 0 |
| `__TEXT` | 160808960 | 0 | 27 |
| `__DATA_CONST` | 7520256 | 160808960 | 15 |
| `__DATA` | 20643840 | 168329216 | 31 |
| `__RODATA` | 24379392 | 183615488 | 5 |
| `__LLVM_COV` | 196608 | 207994880 | 2 |
| `__LINKEDIT` | 15056896 | 208191488 | 0 |

<details><summary>依赖库清单</summary>

- `/usr/lib/libbz2.1.0.dylib` （LC_LOAD_DYLIB）
- `/usr/lib/libc++.1.dylib` （LC_LOAD_DYLIB）
- `/usr/lib/libc++abi.dylib` （LC_LOAD_DYLIB）
- `/usr/lib/libiconv.2.dylib` （LC_LOAD_DYLIB）
- `/usr/lib/libicucore.A.dylib` （LC_LOAD_DYLIB）
- `/usr/lib/libresolv.9.dylib` （LC_LOAD_DYLIB）
- `/usr/lib/libsqlite3.dylib` （LC_LOAD_DYLIB）
- `/usr/lib/swift/libswiftCoreGraphics.dylib` （LC_LOAD_DYLIB）
- `/usr/lib/libxml2.2.dylib` （LC_LOAD_DYLIB）
- `/usr/lib/libz.1.dylib` （LC_LOAD_DYLIB）
- `/System/Library/Frameworks/ARKit.framework/ARKit` （LC_LOAD_WEAK_DYLIB）
- `/System/Library/Frameworks/AVFoundation.framework/AVFoundation` （LC_LOAD_WEAK_DYLIB）
- `/System/Library/Frameworks/AVKit.framework/AVKit` （LC_LOAD_DYLIB）
- `/System/Library/Frameworks/Accelerate.framework/Accelerate` （LC_LOAD_DYLIB）
- `/System/Library/Frameworks/AdSupport.framework/AdSupport` （LC_LOAD_DYLIB）
- `@rpath/AgoraAiEchoCancellationExtension.framework/AgoraAiEchoCancellationExtension` （LC_LOAD_DYLIB）
- `@rpath/AgoraAiNoiseSuppressionExtension.framework/AgoraAiNoiseSuppressionExtension` （LC_LOAD_DYLIB）
- `@rpath/AgoraAudioBeautyExtension.framework/AgoraAudioBeautyExtension` （LC_LOAD_DYLIB）
- `@rpath/AgoraRtcKit.framework/AgoraRtcKit` （LC_LOAD_DYLIB）
- `@rpath/AgoraSoundTouch.framework/AgoraSoundTouch` （LC_LOAD_DYLIB）
- `@rpath/Agorafdkaac.framework/Agorafdkaac` （LC_LOAD_DYLIB）
- `@rpath/Agoraffmpeg.framework/Agoraffmpeg` （LC_LOAD_DYLIB）
- `/System/Library/Frameworks/AssetsLibrary.framework/AssetsLibrary` （LC_LOAD_DYLIB）
- `/System/Library/Frameworks/AudioToolbox.framework/AudioToolbox` （LC_LOAD_WEAK_DYLIB）
- `/System/Library/Frameworks/AuthenticationServices.framework/AuthenticationServices` （LC_LOAD_WEAK_DYLIB）
- `@rpath/ByteRTCFFmpegAudioExtension.framework/ByteRTCFFmpegAudioExtension` （LC_LOAD_DYLIB）
- `/System/Library/Frameworks/CFNetwork.framework/CFNetwork` （LC_LOAD_DYLIB）
- `/System/Library/Frameworks/Contacts.framework/Contacts` （LC_LOAD_DYLIB）
- `/System/Library/Frameworks/CoreAudio.framework/CoreAudio` （LC_LOAD_DYLIB）
- `/System/Library/Frameworks/CoreFoundation.framework/CoreFoundation` （LC_LOAD_DYLIB）
- `/System/Library/Frameworks/CoreGraphics.framework/CoreGraphics` （LC_LOAD_DYLIB）
- `/System/Library/Frameworks/CoreImage.framework/CoreImage` （LC_LOAD_DYLIB）
- `/System/Library/Frameworks/CoreLocation.framework/CoreLocation` （LC_LOAD_DYLIB）
- `/System/Library/Frameworks/CoreML.framework/CoreML` （LC_LOAD_WEAK_DYLIB）
- `/System/Library/Frameworks/CoreMedia.framework/CoreMedia` （LC_LOAD_WEAK_DYLIB）
- `/System/Library/Frameworks/CoreMotion.framework/CoreMotion` （LC_LOAD_WEAK_DYLIB）
- `/System/Library/Frameworks/CoreServices.framework/CoreServices` （LC_LOAD_DYLIB）
- `/System/Library/Frameworks/CoreTelephony.framework/CoreTelephony` （LC_LOAD_WEAK_DYLIB）
- `/System/Library/Frameworks/CoreText.framework/CoreText` （LC_LOAD_DYLIB）
- `/System/Library/Frameworks/CoreVideo.framework/CoreVideo` （LC_LOAD_DYLIB）
- `/System/Library/Frameworks/Foundation.framework/Foundation` （LC_LOAD_DYLIB）
- `/System/Library/Frameworks/GLKit.framework/GLKit` （LC_LOAD_DYLIB）
- `/System/Library/Frameworks/GameController.framework/GameController` （LC_LOAD_DYLIB）
- `/System/Library/Frameworks/GameKit.framework/GameKit` （LC_LOAD_DYLIB）
- `/System/Library/Frameworks/ImageIO.framework/ImageIO` （LC_LOAD_DYLIB）
- `/System/Library/Frameworks/JavaScriptCore.framework/JavaScriptCore` （LC_LOAD_DYLIB）
- `/System/Library/Frameworks/MapKit.framework/MapKit` （LC_LOAD_DYLIB）
- `/System/Library/Frameworks/MediaPlayer.framework/MediaPlayer` （LC_LOAD_DYLIB）
- `/System/Library/Frameworks/MessageUI.framework/MessageUI` （LC_LOAD_DYLIB）
- `/System/Library/Frameworks/Metal.framework/Metal` （LC_LOAD_DYLIB）
- `/System/Library/Frameworks/MetalKit.framework/MetalKit` （LC_LOAD_WEAK_DYLIB）
- `/System/Library/Frameworks/MobileCoreServices.framework/MobileCoreServices` （LC_LOAD_DYLIB）
- `/System/Library/Frameworks/OpenAL.framework/OpenAL` （LC_LOAD_WEAK_DYLIB）
- `/System/Library/Frameworks/OpenGLES.framework/OpenGLES` （LC_LOAD_DYLIB）
- `/System/Library/Frameworks/Photos.framework/Photos` （LC_LOAD_DYLIB）
- `/System/Library/Frameworks/QuartzCore.framework/QuartzCore` （LC_LOAD_DYLIB）
- `@rpath/RTCFFmpeg.framework/RTCFFmpeg` （LC_LOAD_DYLIB）
- `@rpath/RealXBase.framework/RealXBase` （LC_LOAD_DYLIB）
- `/System/Library/Frameworks/ReplayKit.framework/ReplayKit` （LC_LOAD_WEAK_DYLIB）
- `/System/Library/Frameworks/Security.framework/Security` （LC_LOAD_DYLIB）
- `/System/Library/Frameworks/StoreKit.framework/StoreKit` （LC_LOAD_DYLIB）
- `@rpath/SudMGP.framework/SudMGP` （LC_LOAD_DYLIB）
- `/System/Library/Frameworks/SystemConfiguration.framework/SystemConfiguration` （LC_LOAD_WEAK_DYLIB）
- `@rpath/TCGSDK.framework/TCGSDK` （LC_LOAD_DYLIB）
- `@rpath/TTFFmpeg.framework/TTFFmpeg` （LC_LOAD_DYLIB）
- `@rpath/TTSDKBMF.framework/TTSDKBMF` （LC_LOAD_DYLIB）
- `@rpath/TTSDKCore.framework/TTSDKCore` （LC_LOAD_DYLIB）
- `@rpath/TTSDKHttpDNS.framework/TTSDKHttpDNS` （LC_LOAD_DYLIB）
- `@rpath/TTSDKLiveBase.framework/TTSDKLiveBase` （LC_LOAD_DYLIB）
- `@rpath/TTSDKLivePlayerBMF.framework/TTSDKLivePlayerBMF` （LC_LOAD_DYLIB）
- `@rpath/TTSDKLivePlayerNormal.framework/TTSDKLivePlayerNormal` （LC_LOAD_DYLIB）
- `@rpath/TTSDKLivePullVolcLog.framework/TTSDKLivePullVolcLog` （LC_LOAD_DYLIB）
- `@rpath/TTSDKPlayer.framework/TTSDKPlayer` （LC_LOAD_DYLIB）
- `@rpath/TTSDKPlayerCoreNormal.framework/TTSDKPlayerCoreNormal` （LC_LOAD_DYLIB）
- `@rpath/TTSDKQuicCore.framework/TTSDKQuicCore` （LC_LOAD_DYLIB）
- `@rpath/TTSDKQuicPull.framework/TTSDKQuicPull` （LC_LOAD_DYLIB）
- `@rpath/TTSDKReachability.framework/TTSDKReachability` （LC_LOAD_DYLIB）
- `@rpath/TTSDKStrategyPull.framework/TTSDKStrategyPull` （LC_LOAD_DYLIB）
- `@rpath/TTSDKTTFFmpegNormal.framework/TTSDKTTFFmpegNormal` （LC_LOAD_DYLIB）
- `@rpath/TTSDKTools.framework/TTSDKTools` （LC_LOAD_DYLIB）
- `@rpath/TTSDKTopSignature.framework/TTSDKTopSignature` （LC_LOAD_DYLIB）
- `@rpath/TTSDKVCN.framework/TTSDKVCN` （LC_LOAD_DYLIB）
- `@rpath/TTSDKVolcLog.framework/TTSDKVolcLog` （LC_LOAD_DYLIB）
- `@rpath/TWEBRTC.framework/TWEBRTC` （LC_LOAD_DYLIB）
- `/System/Library/Frameworks/UIKit.framework/UIKit` （LC_LOAD_DYLIB）
- `/System/Library/Frameworks/UserNotifications.framework/UserNotifications` （LC_LOAD_DYLIB）
- `/System/Library/Frameworks/VideoToolbox.framework/VideoToolbox` （LC_LOAD_WEAK_DYLIB）
- `@rpath/VolcBaseLog.framework/VolcBaseLog` （LC_LOAD_DYLIB）
- `@rpath/VolcEngineRTC.framework/VolcEngineRTC` （LC_LOAD_DYLIB）
- `/System/Library/Frameworks/WebKit.framework/WebKit` （LC_LOAD_DYLIB）
- `@rpath/aosl.framework/aosl` （LC_LOAD_DYLIB）
- `@rpath/bytenn.framework/bytenn` （LC_LOAD_DYLIB）
- `@rpath/h265enc.framework/h265enc` （LC_LOAD_DYLIB）
- `@rpath/libvcn.framework/libvcn` （LC_LOAD_DYLIB）
- `@rpath/nuisdk.framework/nuisdk` （LC_LOAD_DYLIB）
- `@rpath/ttboringssl.framework/ttboringssl` （LC_LOAD_DYLIB）
- `@rpath/ttcrypto.framework/ttcrypto` （LC_LOAD_DYLIB）
- `/System/Library/Frameworks/AppTrackingTransparency.framework/AppTrackingTransparency` （LC_LOAD_WEAK_DYLIB）
- `/System/Library/Frameworks/CoreHaptics.framework/CoreHaptics` （LC_LOAD_WEAK_DYLIB）
- `/System/Library/Frameworks/DeviceCheck.framework/DeviceCheck` （LC_LOAD_WEAK_DYLIB）
- `/System/Library/Frameworks/MetalPerformanceShaders.framework/MetalPerformanceShaders` （LC_LOAD_WEAK_DYLIB）
- `/System/Library/Frameworks/MetricKit.framework/MetricKit` （LC_LOAD_WEAK_DYLIB）
- `/System/Library/Frameworks/Vision.framework/Vision` （LC_LOAD_WEAK_DYLIB）
- `/System/Library/Frameworks/UniformTypeIdentifiers.framework/UniformTypeIdentifiers` （LC_LOAD_WEAK_DYLIB）
- `/System/Library/Frameworks/PhotosUI.framework/PhotosUI` （LC_LOAD_WEAK_DYLIB）
- `/System/Library/Frameworks/SceneKit.framework/SceneKit` （LC_LOAD_WEAK_DYLIB）
- `/System/Library/Frameworks/EventKit.framework/EventKit` （LC_LOAD_DYLIB）
- `/System/Library/Frameworks/WatchConnectivity.framework/WatchConnectivity` （LC_LOAD_DYLIB）
- `/System/Library/Frameworks/AddressBook.framework/AddressBook` （LC_LOAD_DYLIB）
- `/System/Library/Frameworks/AddressBookUI.framework/AddressBookUI` （LC_LOAD_DYLIB）
- `/System/Library/Frameworks/CoreData.framework/CoreData` （LC_LOAD_DYLIB）
- `/usr/lib/libobjc.A.dylib` （LC_LOAD_DYLIB）
- `/usr/lib/libSystem.B.dylib` （LC_LOAD_DYLIB）
- `/System/Library/Frameworks/AVFAudio.framework/AVFAudio` （LC_LOAD_WEAK_DYLIB）
- `/System/Library/Frameworks/AdServices.framework/AdServices` （LC_LOAD_DYLIB）
- `/System/Library/Frameworks/Combine.framework/Combine` （LC_LOAD_DYLIB）
- `/System/Library/Frameworks/ContactsUI.framework/ContactsUI` （LC_LOAD_DYLIB）
- `/System/Library/Frameworks/ExternalAccessory.framework/ExternalAccessory` （LC_LOAD_DYLIB）
- `/System/Library/Frameworks/LocalAuthentication.framework/LocalAuthentication` （LC_LOAD_DYLIB）
- `/System/Library/Frameworks/MediaToolbox.framework/MediaToolbox` （LC_LOAD_DYLIB）
- `/System/Library/Frameworks/Network.framework/Network` （LC_LOAD_DYLIB）
- `/System/Library/Frameworks/QuickLook.framework/QuickLook` （LC_LOAD_DYLIB）
- `/System/Library/Frameworks/SafariServices.framework/SafariServices` （LC_LOAD_DYLIB）
- `/System/Library/Frameworks/SwiftUI.framework/SwiftUI` （LC_LOAD_DYLIB）
- `/usr/lib/libcompression.dylib` （LC_LOAD_WEAK_DYLIB）
- `/usr/lib/swift/libswiftARKit.dylib` （LC_LOAD_WEAK_DYLIB）
- `/usr/lib/swift/libswiftAVFoundation.dylib` （LC_LOAD_WEAK_DYLIB）
- `/usr/lib/swift/libswiftAccelerate.dylib` （LC_LOAD_WEAK_DYLIB）
- `/usr/lib/swift/libswiftCore.dylib` （LC_LOAD_DYLIB）
- `/usr/lib/swift/libswiftCoreAudio.dylib` （LC_LOAD_WEAK_DYLIB）
- `/usr/lib/swift/libswiftCoreFoundation.dylib` （LC_LOAD_DYLIB）
- `/usr/lib/swift/libswiftCoreImage.dylib` （LC_LOAD_WEAK_DYLIB）
- `/usr/lib/swift/libswiftCoreLocation.dylib` （LC_LOAD_WEAK_DYLIB）
- `/usr/lib/swift/libswiftCoreMIDI.dylib` （LC_LOAD_WEAK_DYLIB）
- `/usr/lib/swift/libswiftCoreMedia.dylib` （LC_LOAD_DYLIB）
- `/usr/lib/swift/libswiftDarwin.dylib` （LC_LOAD_DYLIB）
- `/usr/lib/swift/libswiftDispatch.dylib` （LC_LOAD_DYLIB）
- `/usr/lib/swift/libswiftGLKit.dylib` （LC_LOAD_WEAK_DYLIB）
- `/usr/lib/swift/libswiftIntents.dylib` （LC_LOAD_WEAK_DYLIB）
- `/usr/lib/swift/libswiftMapKit.dylib` （LC_LOAD_WEAK_DYLIB）
- `/usr/lib/swift/libswiftMetal.dylib` （LC_LOAD_WEAK_DYLIB）
- `/usr/lib/swift/libswiftMetalKit.dylib` （LC_LOAD_WEAK_DYLIB）
- `/usr/lib/swift/libswiftModelIO.dylib` （LC_LOAD_WEAK_DYLIB）
- `/usr/lib/swift/libswiftOSLog.dylib` （LC_LOAD_WEAK_DYLIB）
- `/usr/lib/swift/libswiftObjectiveC.dylib` （LC_LOAD_DYLIB）
- `/usr/lib/swift/libswiftQuartzCore.dylib` （LC_LOAD_WEAK_DYLIB）
- `/usr/lib/swift/libswiftSceneKit.dylib` （LC_LOAD_WEAK_DYLIB）
- `/usr/lib/swift/libswiftSpatial.dylib` （LC_LOAD_WEAK_DYLIB）
- `/usr/lib/swift/libswiftSpriteKit.dylib` （LC_LOAD_WEAK_DYLIB）
- `/usr/lib/swift/libswiftUniformTypeIdentifiers.dylib` （LC_LOAD_WEAK_DYLIB）
- `/usr/lib/swift/libswiftXPC.dylib` （LC_LOAD_WEAK_DYLIB）
- `/usr/lib/swift/libswift_Concurrency.dylib` （LC_LOAD_WEAK_DYLIB）
- `/usr/lib/swift/libswiftos.dylib` （LC_LOAD_WEAK_DYLIB）
- `/usr/lib/swift/libswiftsimd.dylib` （LC_LOAD_WEAK_DYLIB）
- `/usr/lib/swift/libswiftFoundation.dylib` （LC_LOAD_DYLIB）
- `/usr/lib/swift/libswiftUIKit.dylib` （LC_LOAD_DYLIB）

</details>

**防护/运行时检测字符串观察**（仅统计字面量出现次数，不做绕过推断）

| 关键字 | 出现次数 |
| --- | ---: |
| `NSURLSession` | 162 |
| `ATS` | 46 |
| `CFNetwork` | 21 |
| `sysctl` | 17 |
| `Substrate` | 12 |
| `MobileSubstrate` | 9 |
| `cydia` | 6 |
| `objc_msgSend` | 6 |
| `jailbreak` | 5 |
| `SSLSetSessionOption` | 5 |
| `SecTrustEvaluate` | 4 |
| `frida` | 3 |
| `jailbroken` | 3 |
| `ptrace` | 2 |
| `Jailbreak` | 2 |
| `posix_spawn` | 2 |
| `DYLD_INSERT_LIBRARIES` | 1 |
| `Frida` | 1 |
| `amfid` | 1 |
| `/Applications/Cydia.app` | 1 |
| `fork()` | 1 |

---

本报告只记录文件结构与公开元数据，用于学习 iOS 二进制组织方式与安全加固现状；
不包含、也不构成对任何技术措施的规避方法。
