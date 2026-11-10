# iOS 二进制深度静态结构报告

- 生成时间：2026-11-10T11:54:12.888698+08:00
- 输入：`E:\iOS-App-Analysis\01-IPA\Soul_6.41.0.ipa`
- 大小：209.94 MiB
- SHA-256：`84497208f44b7cc459eeede5ef93b2339690bf5e61773a949e5b24f47878f4f0`

> 范围声明：本报告只记录文件内静态结构与公开元数据（架构、节、符号统计、签名、依赖）。
> 不含反编译伪代码，不逐条列出业务类名/方法名，不定位任何业务方法，
> 不提供规避技术措施的指引。

## 1. 应用元数据

| 字段 | 值 |
| --- | --- |
| `CFBundleIdentifier` | com.soulapp.cn |
| `CFBundleExecutable` | Soul_New |
| `CFBundleShortVersionString` | 6.41.0 |
| `CFBundleVersion` | 261029205000 |
| `MinimumOSVersion` | 15.0 |
| `CFBundleSupportedPlatforms` | ['iPhoneOS'] |
| `UIDeviceFamily` | [1, 2] |
| `ITSAppUsesNonExemptEncryption` | False |
| `NSAppTransportSecurity` | {'NSAllowsArbitraryLoads': True, 'NSExceptionDomains': {'sinaimg.cn': {'NSThirdPartyExceptionAllowsInsecureHTTPLoads': True, 'NSThirdPartyExceptionRequiresForwardSecrecy': False, ' ... |
| `CFBundleURLTypes` | [{'CFBundleTypeRole': 'Editor', 'CFBundleURLName': 'wechat', 'CFBundleURLSchemes': ['wxcc5f58957efdffe9']}, {'CFBundleTypeRole': 'Editor', 'CFBundleURLSchemes': ['QQ41df0edc']}, {' ... |
| `UIRequiredDeviceCapabilities` | ['arm64'] |
| `LSRequiresIPhoneOS` | True |
| `NSCameraUsageDescription` | 为了您能正常体验拍照、录制视频/表情包、视频匹配、扫一扫等功能，Soul需要申请相机权限。如您拒绝授权，不影响您使用APP的其他功能。 |
| `NSPhotoLibraryUsageDescription` | 为了您能正常分享图片/视频、保存图片/视频，Soul需要申请存储权限。如您拒绝授权，不影响您使用APP的其他功能。 |
| `NSMicrophoneUsageDescription` | 为了您能正常体验语音输入、语音变声、语音匹配、视频匹配等功能，Soul需要申请麦克风权限。如您拒绝授权，不影响您使用APP的其他功能。 |
| `executable` | Payload/Soul_New.app/Soul_New |
| `executable_size` | 217173488 |

## 2. 包内容分布

- IPA 条目数：**4094**
- 内嵌 framework：**39** 个；内嵌 dylib：**0** 个
- App Extension：**5** 个 ['IntentHandler.appex', 'SoulBroadcastExtension.appex', 'SoulPushExtension.appex', 'SoulShareExtension.appex', 'SoulWidgetExtension.appex']
- 描述文件：无／代码签名目录：有／隐私清单：有
- Assets.car：有／编译 nib/storyboard：有

<details><summary>内嵌 framework 清单</summary>

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
- `VolcEngineRTC.framework`
- `XMagic.framework`
- `YTCommonXMagic.framework`
- `bytenn.framework`
- `hermes.framework`
- `libpag.framework`
- `libvcn.framework`
- `ttboringssl.framework`
- `ttcrypto.framework`

</details>

### 文件类型分布（前 14）

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
| `.car` | 27 |
| `.xcprivacy` | 24 |

## 3. Mach-O 内部结构（容器：thin）

### 切片 single

- CPU：`ARM64` / 子类型 `0x0` / 类型 `MH_EXECUTE`
- 加载命令 **175** 条（17744 字节）；标志：MH_NOUNDEFS, MH_DYLD_LINK, MH_TWOLEVEL, MH_WEAK_DEFINES, MH_BINDS_TO_WEAK, MH_PIE
- UUID：`D88E6E6C754B3C7EBC80F6F879AD3C12`；构建：`{'platform': 'iOS', 'minos': '15.0.0', 'sdk': '27.1.0', 'ntools': 1}`
- 加密：`not encrypted (decrypted image)`；PIE：**是**

**加载命令构成**

| 命令 | 条数 |
| --- | ---: |
| `LC_LOAD_DYLIB` | 107 |
| `LC_LOAD_WEAK_DYLIB` | 47 |
| `LC_SEGMENT_64` | 5 |
| `LC_RPATH` | 3 |
| `LC_DYLD_CHAINED_FIXUPS` | 1 |
| `LC_DYLD_EXPORTS_TRIE` | 1 |
| `LC_SYMTAB` | 1 |
| `LC_DYSYMTAB` | 1 |
| `LC_LOAD_DYLINKER` | 1 |
| `LC_UUID` | 1 |
| `LC_BUILD_VERSION` | 1 |
| `LC_SOURCE_VERSION` | 1 |
| `LC_0x80000028` | 1 |
| `LC_ENCRYPTION_INFO_64` | 1 |
| `LC_FUNCTION_STARTS` | 1 |
| `LC_DATA_IN_CODE` | 1 |
| `LC_CODE_SIGNATURE` | 1 |

**段表**

| 段 | VM 大小 | 文件偏移 | 文件大小 | 节数 | 初始保护 |
| --- | ---: | ---: | ---: | ---: | ---: |
| `__PAGEZERO` | 4,294,967,296 | 0 | 0 | 0 | 0 |
| `__TEXT` | 169,902,080 | 0 | 169,902,080 | 31 | 5 |
| `__DATA_CONST` | 7,454,720 | 169,902,080 | 7,454,720 | 15 | 3 |
| `__DATA` | 31,293,440 | 177,356,800 | 27,820,032 | 20 | 3 |
| `__LINKEDIT` | 12,009,472 | 205,176,832 | 11,996,656 | 0 | 1 |

**节表**：共 66 节

| 段,节 | 大小 | 地址 |
| --- | ---: | --- |
| `__TEXT,__text` | 139,307,672 | `0x100008000` |
| `__DATA,__objc_const` | 17,737,776 | `0x10a924000` |
| `__TEXT,__objc_methname` | 7,623,837 | `0x1094bfe10` |
| `__DATA,__objc_data` | 5,110,792 | `0x10bbce7b0` |
| `__TEXT,__objc_stubs` | 4,458,464 | `0x1084ef8a0` |
| `__TEXT,__cstring` | 4,185,528 | `0x10907e350` |
| `__DATA_CONST,__const` | 3,929,400 | `0x10a208000` |
| `__TEXT,__const` | 3,810,719 | `0x108933ac0` |
| `__DATA,__data` | 3,121,085 | `0x10c0ae400` |
| `__DATA_CONST,__cfstring` | 2,833,984 | `0x10a5c7538` |
| `__DATA,__bss` | 2,777,496 | `0x10c3a8b00` |
| `__TEXT,__gcc_except_tab` | 2,586,504 | `0x109c05f70` |
| `__TEXT,__unwind_info` | 2,375,520 | `0x109f2ab50` |
| `__DATA,__objc_selrefs` | 1,221,680 | `0x10ba0e830` |

**符号表**

- 符号总数：**7,727**；ObjC 类符号：**594**

| 符号类型 | 数量 |
| --- | ---: |
| `N_UNDF (undefined/import)` | 7,067 |
| `N_SECT (defined)` | 659 |
| `N_PBUD` | 1 |

| 符号归类 | 数量 |
| --- | ---: |
| `other` | 3,257 |
| `cpp_mangled` | 1,922 |
| `swift_mangled` | 1,779 |
| `objc_class` | 594 |
| `objc_metaclass` | 96 |
| `objc_runtime` | 79 |

类符号前缀聚类（仅统计，不输出业务类名）：`UI`(134)、`NS`(123)、`AV`(44)、`IESMM`(28)、`Byte`(22)、`VE`(22)、`PH`(21)、`CA`(18)、`Agora`(17)、`IN`(14)、`GDT`(11)、`IES`(9)、`CI`(7)、`EK`(7)

**Objective-C / Swift 元数据**

| 指标 | 值 |
| --- | ---: |
| `__objc_*` 节数 | 13 |
| 类名字符串数 | 25,977 |
| 方法名字符串数 | 311,819 |
| classlist 条目 | 21,292 |
| selector 引用 | 152,710 |
| class 引用 | 15,938 |
| category / protocol | 442 / 3,339 |
| Swift `__swift5_*` 节数 | 10 |

<details><summary>ObjC 节及大小</summary>

- `__DATA,__objc_classrefs` — 127,504 B
- `__DATA,__objc_const` — 17,737,776 B
- `__DATA,__objc_data` — 5,110,792 B
- `__DATA,__objc_ivar` — 398,928 B
- `__DATA,__objc_protorefs` — 11,696 B
- `__DATA,__objc_selrefs` — 1,221,680 B
- `__DATA,__objc_superrefs` — 75,072 B
- `__DATA_CONST,__objc_catlist` — 3,536 B
- `__DATA_CONST,__objc_classlist` — 170,336 B
- `__DATA_CONST,__objc_imageinfo` — 8 B
- `__DATA_CONST,__objc_protolist` — 26,712 B
- `__TEXT,__objc_classname` — 706,447 B
- `__TEXT,__objc_methname` — 7,623,837 B

</details>

**静态字符串节**

| 节 | 大小 | 字符串数 | 平均长度 | 最长 |
| --- | ---: | ---: | ---: | ---: |
| `__TEXT,__const` | 3,810,719 | — | — | — |
| `__TEXT,__cstring` | 4,185,528 | 123103 | 31.7 | 18679 |
| `__TEXT,__ustring` | 706,946 | — | — | — |
| `__DATA_CONST,__const` | 3,929,400 | — | — | — |
| `__DATA_CONST,__cfstring` | 2,833,984 | — | — | — |

**代码签名**

- SuperBlob：`0xfade0cc0`；blob 数 6

- `CodeDirectory`（0xfade0c02）：标识 `com.soulapp.cn`，SHA-1，page 4096 B，codeSlots 51,704，TeamID `M45G2F887R`，布局 `length-prefixed`
- `Requirements`（0xfade0c01）
- `Entitlements`（0xfade7171）
- `DEREntitlements`（0xfade7172）
- `AlternateCodeDirectory`（0xfade0c02）：标识 `com.soulapp.cn`，SHA-256，page 4096 B，codeSlots 51,704，TeamID `M45G2F887R`，布局 `length-prefixed`
- `CMSSignature`（0xfade0b01）

 entitlements 键：`application-identifier`、`aps-environment`、`com.apple.developer.applesignin`、`com.apple.developer.associated-domains`、`com.apple.developer.kernel.extended-virtual-addressing`、`com.apple.developer.kernel.increased-memory-limit`、`com.apple.developer.networking.wifi-info`、`com.apple.developer.team-identifier`、`com.apple.developer.usernotifications.communication`、`com.apple.developer.usernotifications.time-sensitive`、`com.apple.security.application-groups`

**导出表（exports trie）**

- 大小 4,622,152 B；遍历节点 1,009；导出符号约 **659** 个（符号名未留存）

**LINKEDIT 数据区**

| 区域 | 偏移 | 大小 |
| --- | ---: | ---: |
| `chained_fixups` | 205,176,832 | 382,208 |
| `exports_trie` | 205,559,040 | 4,622,152 |
| `function_starts` | 210,181,192 | 1,100,648 |
| `data_in_code` | 211,281,840 | 304 |
| `code_signature` | 211,775,760 | 5,397,728 |

**依赖库归类**

| 类别 | 数量 |
| --- | ---: |
| `system_frameworks` | 68 |
| `system_libs` | 12 |
| `embedded` | 39 |
| `third_party` | 0 |
| `swift_runtime` | 35 |

<details><summary>内嵌/第三方动态库路径</summary>

- `@rpath/AdjustSigSdk.framework/AdjustSigSdk`
- `@rpath/AgoraAudioBeautyExtension.framework/AgoraAudioBeautyExtension`
- `@rpath/AgoraRtcKit.framework/AgoraRtcKit`
- `@rpath/AgoraSoundTouch.framework/AgoraSoundTouch`
- `@rpath/Agorafdkaac.framework/Agorafdkaac`
- `@rpath/Agoraffmpeg.framework/Agoraffmpeg`
- `@rpath/ByteRTCFFmpegAudioExtension.framework/ByteRTCFFmpegAudioExtension`
- `@rpath/CFGameSDK.framework/CFGameSDK`
- `@rpath/GDTMobSDK.framework/GDTMobSDK`
- `@rpath/GTNetwork.framework/GTNetwork`
- `@rpath/OpenSSL.framework/OpenSSL`
- `@rpath/RTCFFmpeg.framework/RTCFFmpeg`
- `@rpath/RealXBase.framework/RealXBase`
- `@rpath/SLFFmpeg.framework/SLFFmpeg`
- `@rpath/TECodec.framework/TECodec`
- `@rpath/TTFFmpeg.framework/TTFFmpeg`
- `@rpath/TTSDKCore.framework/TTSDKCore`
- `@rpath/TTSDKPlayer.framework/TTSDKPlayer`
- `@rpath/TTSDKPlayerCoreNormal.framework/TTSDKPlayerCoreNormal`
- `@rpath/TTSDKReachability.framework/TTSDKReachability`
- `@rpath/TTSDKTTFFmpegNormal.framework/TTSDKTTFFmpegNormal`
- `@rpath/TTSDKTools.framework/TTSDKTools`
- `@rpath/TTSDKTopSignature.framework/TTSDKTopSignature`
- `@rpath/TTSDKVCN.framework/TTSDKVCN`
- `@rpath/TTSDKVolcLog.framework/TTSDKVolcLog`
- `@rpath/TXFFmpeg.framework/TXFFmpeg`
- `@rpath/TXSoundTouch.framework/TXSoundTouch`
- `@rpath/Tquic.framework/Tquic`
- `@rpath/VolcBaseLog.framework/VolcBaseLog`
- `@rpath/VolcEngineRTC.framework/VolcEngineRTC`
- `@rpath/XMagic.framework/XMagic`
- `@rpath/YTCommonXMagic.framework/YTCommonXMagic`
- `@rpath/bytenn.framework/bytenn`
- `@rpath/hermes.framework/hermes`
- `@rpath/libpag.framework/libpag`
- `@rpath/libvcn.framework/libvcn`
- `@rpath/ttboringssl.framework/ttboringssl`
- `@rpath/ttcrypto.framework/ttcrypto`
- `@rpath/TTVideoEditor.framework/TTVideoEditor`

</details>

**公开技术机制观察**（仅依据符号/节名是否存在，不作绕过推断）

| 类别 | 命中的符号 |
| --- | --- |
| `stack_protector` | `___stack_chk_guard` |
| `arc_objc` | `_objc_autoreleasePoolPush`, `_objc_release`, `_objc_retain` |
| `objc_runtime` | `_objc_allocateClassPair`, `_objc_getClass`, `_objc_msgSend` |
| `ptrace_debug` | `_sysctl` |
| `trust_eval` | `_SSLCreateContext`, `_SSLSetSessionOption`, `_SecTrustEvaluate`, `_SecTrustEvaluateWithError` |
| `dyld_introspection` | `_dlopen`, `_dlsym` |
| `crypto_common` | `_CCCrypt`, `_CC_MD5`, `_CC_SHA1` |
| `keychain` | `_SecItemAdd`, `_SecItemCopyMatching` |

**技术栈推断**：Objective-C（__objc_* 元数据节 + ObjC 类符号）；Swift（__swift5_* 节 / Swift mangled 符号 / libswift 运行时）；C/C++（Itanium mangled 符号）；Hermes JS 引擎（依赖库线索）；JavaScriptCore（依赖库线索）；原生编译产物（__cstring 等静态字符串节）

> 静态节名 / 符号前缀 / 依赖库路径，仅为线索，不代表运行时行为

---

本报告由只读静态解析生成，用于学习 iOS 二进制组织方式与工程实践；
不包含、也不构成对任何技术措施的规避方法。
