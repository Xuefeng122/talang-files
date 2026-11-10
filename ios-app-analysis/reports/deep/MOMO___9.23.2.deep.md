# iOS 二进制深度静态结构报告

- 生成时间：2026-11-10T11:54:08.697543+08:00
- 输入：`E:\iOS-App-Analysis\01-IPA\MOMO陌陌_9.23.2.ipa`
- 大小：157.55 MiB
- SHA-256：`fe86448b141057ee8ac79bd67ac7a3b79e247af14c87dce8d1f03524a33ae487`

> 范围声明：本报告只记录文件内静态结构与公开元数据（架构、节、符号统计、签名、依赖）。
> 不含反编译伪代码，不逐条列出业务类名/方法名，不定位任何业务方法，
> 不提供规避技术措施的指引。

## 1. 应用元数据

| 字段 | 值 |
| --- | --- |
| `CFBundleIdentifier` | com.wemomo.momoappdemo1 |
| `CFBundleExecutable` | MomoChat |
| `CFBundleShortVersionString` | 9.23.2 |
| `CFBundleVersion` | 9.23.2.7 |
| `MinimumOSVersion` | 15.0 |
| `CFBundleSupportedPlatforms` | ['iPhoneOS'] |
| `UIDeviceFamily` | [1] |
| `ITSAppUsesNonExemptEncryption` | False |
| `NSAppTransportSecurity` | {'NSAllowsArbitraryLoads': True} |
| `CFBundleURLTypes` | [{'CFBundleTypeRole': 'Editor', 'CFBundleURLName': 'com.immomo.momo', 'CFBundleURLSchemes': ['momologinauthorize', 'momochatsdk', 'momochs', 'momoSDK', 'wb2041542309', 'rm165934com ... |
| `UIRequiredDeviceCapabilities` | ['arm64'] |
| `LSRequiresIPhoneOS` | True |
| `NSCameraUsageDescription` | 您还没有开启相机权限，开启后才能正常拍摄照片、视频进行发布，或者通过直播实时分享生活。 |
| `NSPhotoLibraryUsageDescription` | 为了您能正常使用编辑头像、发布动态、发送聊天图片/视频等功能，MOMO陌陌需要申请相册权限。 |
| `NSMicrophoneUsageDescription` | 您还没有开启麦克风权限，开启后才能在正常拍摄视频时录制声音，或者直播时分享声音。 |
| `executable` | Payload/MomoChat.app/MomoChat |
| `executable_size` | 223240448 |

## 2. 包内容分布

- IPA 条目数：**2725**
- 内嵌 framework：**41** 个；内嵌 dylib：**0** 个
- App Extension：**1** 个 ['MDNotificationService.appex']
- 描述文件：无／代码签名目录：有／隐私清单：有
- Assets.car：有／编译 nib/storyboard：有

<details><summary>内嵌 framework 清单</summary>

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
- `TTSDKVolcLog.framework`
- `TWEBRTC.framework`
- `VolcBaseLog.framework`
- `VolcEngineRTC.framework`
- `aosl.framework`
- `bytenn.framework`
- `h265enc.framework`
- `libvcn.framework`
- `nuisdk.framework`
- `ttboringssl.framework`
- `ttcrypto.framework`

</details>

### 文件类型分布（前 14）

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
| `.caf` | 16 |
| `.rtg` | 16 |

## 3. Mach-O 内部结构（容器：thin）

### 切片 single

- CPU：`ARM64` / 子类型 `0x0` / 类型 `MH_EXECUTE`
- 加载命令 **179** 条（19424 字节）；标志：MH_NOUNDEFS, MH_DYLD_LINK, MH_TWOLEVEL, MH_WEAK_DEFINES, MH_BINDS_TO_WEAK, MH_PIE
- UUID：`94F4545CB80F3AA3B61AA403A0FBBC19`；构建：`{'platform': 'iOS', 'minos': '15.0.0', 'sdk': '26.2.0', 'ntools': 4}`
- 加密：`not encrypted (decrypted image)`；PIE：**是**

**加载命令构成**

| 命令 | 条数 |
| --- | ---: |
| `LC_LOAD_DYLIB` | 109 |
| `LC_LOAD_WEAK_DYLIB` | 47 |
| `LC_SEGMENT_64` | 7 |
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
| `__TEXT` | 160,808,960 | 0 | 160,808,960 | 27 | 5 |
| `__DATA_CONST` | 7,520,256 | 160,808,960 | 7,520,256 | 15 | 3 |
| `__DATA` | 20,643,840 | 168,329,216 | 15,253,504 | 31 | 3 |
| `__RODATA` | 24,379,392 | 183,615,488 | 24,379,392 | 5 | 3 |
| `__LLVM_COV` | 196,608 | 207,994,880 | 196,608 | 2 | 3 |
| `__LINKEDIT` | 15,056,896 | 208,191,488 | 15,048,960 | 0 | 1 |

**节表**：共 80 节

| 段,节 | 大小 | 地址 |
| --- | ---: | --- |
| `__TEXT,__text` | 146,000,396 | `0x100008000` |
| `__RODATA,__const` | 9,164,369 | `0x10c2b7500` |
| `__DATA,__objc_const` | 9,135,464 | `0x10a088000` |
| `__RODATA,__cstring` | 7,204,591 | `0x10bbd85e0` |
| `__RODATA,__objc_methname` | 6,743,394 | `0x10b4ae320` |
| `__TEXT,__objc_methlist` | 4,620,708 | `0x108f8bb80` |
| `__DATA_CONST,__const` | 4,540,440 | `0x109983b80` |
| `__TEXT,__objc_stubs` | 4,392,960 | `0x108b585a0` |
| `__DATA,__bss` | 3,896,376 | `0x10af14000` |
| `__DATA_CONST,__cfstring` | 2,576,224 | `0x109dd8398` |
| `__TEXT,__gcc_except_tab` | 2,163,032 | `0x10940c998` |
| `__DATA,__data` | 1,936,809 | `0x10ad29be0` |
| `__DATA,__objc_data` | 1,833,208 | `0x10ab373c0` |
| `__TEXT,__unwind_info` | 1,801,516 | `0x10971aed8` |

**符号表**

- 符号总数：**12,789**；ObjC 类符号：**537**

| 符号类型 | 数量 |
| --- | ---: |
| `N_SECT (defined)` | 7,294 |
| `N_UNDF (undefined/import)` | 5,494 |
| `N_PBUD` | 1 |

| 符号归类 | 数量 |
| --- | ---: |
| `cpp_mangled` | 7,623 |
| `other` | 3,141 |
| `swift_mangled` | 1,329 |
| `objc_class` | 537 |
| `objc_metaclass` | 84 |
| `objc_runtime` | 75 |

类符号前缀聚类（仅统计，不输出业务类名）：`NS`(126)、`UI`(115)、`AV`(48)、`MTL`(31)、`Byte`(25)、`CA`(18)、`PH`(16)、`Agora`(14)、`MPSCNN`(12)、`SK`(9)、`MP`(8)、`MPS`(8)、`WK`(8)、`CI`(7)

**Objective-C / Swift 元数据**

| 指标 | 值 |
| --- | ---: |
| `__objc_*` 节数 | 13 |
| 类名字符串数 | 23,100 |
| 方法名字符串数 | 289,676 |
| classlist 条目 | 18,299 |
| selector 引用 | 183,595 |
| class 引用 | 15,269 |
| category / protocol | 1,318 / 2,675 |
| Swift `__swift5_*` 节数 | 10 |

<details><summary>ObjC 节及大小</summary>

- `__DATA,__objc_classrefs` — 122,152 B
- `__DATA,__objc_const` — 9,135,464 B
- `__DATA,__objc_data` — 1,833,208 B
- `__DATA,__objc_ivar` — 388,496 B
- `__DATA,__objc_protorefs` — 3,912 B
- `__DATA,__objc_selrefs` — 1,468,760 B
- `__DATA,__objc_superrefs` — 84,736 B
- `__DATA_CONST,__objc_catlist` — 10,544 B
- `__DATA_CONST,__objc_classlist` — 146,392 B
- `__DATA_CONST,__objc_imageinfo` — 8 B
- `__DATA_CONST,__objc_protolist` — 21,400 B
- `__RODATA,__objc_classname` — 484,127 B
- `__RODATA,__objc_methname` — 6,743,394 B

</details>

**静态字符串节**

| 节 | 大小 | 字符串数 | 平均长度 | 最长 |
| --- | ---: | ---: | ---: | ---: |
| `__TEXT,__const` | 101,480 | — | — | — |
| `__TEXT,__ustring` | 421,008 | — | — | — |
| `__DATA_CONST,__const` | 4,540,440 | — | — | — |
| `__DATA_CONST,__cfstring` | 2,576,224 | — | — | — |
| `__RODATA,__cstring` | 7,204,591 | 187397 | 37.1 | 355208 |
| `__RODATA,__const` | 9,164,369 | — | — | — |

**代码签名**

- SuperBlob：`0xfade0cc0`；blob 数 6

- `CodeDirectory`（0xfade0c02）：标识 `com.wemomo.momoappdemo1`，SHA-1，page 4096 B，codeSlots 53,148，TeamID `36WT396TPZ`，布局 `length-prefixed`
- `Requirements`（0xfade0c01）
- `Entitlements`（0xfade7171）
- `DEREntitlements`（0xfade7172）
- `AlternateCodeDirectory`（0xfade0c02）：标识 `com.wemomo.momoappdemo1`，SHA-256，page 4096 B，codeSlots 53,148，TeamID `36WT396TPZ`，布局 `length-prefixed`
- `CMSSignature`（0xfade0b01）

 entitlements 键：`application-identifier`、`aps-environment`、`com.apple.developer.applesignin`、`com.apple.developer.associated-appclip-app-identifiers`、`com.apple.developer.associated-domains`、`com.apple.developer.kernel.extended-virtual-addressing`、`com.apple.developer.kernel.increased-memory-limit`、`com.apple.developer.networking.multicast`、`com.apple.developer.networking.wifi-info`、`com.apple.developer.team-identifier`、`com.apple.developer.usernotifications.communication`、`com.apple.security.application-groups`

**导出表（exports trie）**

- 大小 6,082,520 B；遍历节点 11,208；导出符号约 **7,294** 个（符号名未留存）

**LINKEDIT 数据区**

| 区域 | 偏移 | 大小 |
| --- | ---: | ---: |
| `chained_fixups` | 208,191,488 | 1,007,032 |
| `exports_trie` | 209,198,520 | 6,082,520 |
| `function_starts` | 215,281,040 | 1,281,736 |
| `data_in_code` | 216,562,776 | 5,096 |
| `code_signature` | 217,691,936 | 5,548,512 |

**依赖库归类**

| 类别 | 数量 |
| --- | ---: |
| `system_frameworks` | 71 |
| `system_libs` | 12 |
| `embedded` | 41 |
| `third_party` | 0 |
| `swift_runtime` | 32 |

<details><summary>内嵌/第三方动态库路径</summary>

- `@rpath/AgoraAiEchoCancellationExtension.framework/AgoraAiEchoCancellationExtension`
- `@rpath/AgoraAiNoiseSuppressionExtension.framework/AgoraAiNoiseSuppressionExtension`
- `@rpath/AgoraAudioBeautyExtension.framework/AgoraAudioBeautyExtension`
- `@rpath/AgoraRtcKit.framework/AgoraRtcKit`
- `@rpath/AgoraSoundTouch.framework/AgoraSoundTouch`
- `@rpath/Agorafdkaac.framework/Agorafdkaac`
- `@rpath/Agoraffmpeg.framework/Agoraffmpeg`
- `@rpath/ByteRTCFFmpegAudioExtension.framework/ByteRTCFFmpegAudioExtension`
- `@rpath/RTCFFmpeg.framework/RTCFFmpeg`
- `@rpath/RealXBase.framework/RealXBase`
- `@rpath/SudMGP.framework/SudMGP`
- `@rpath/TCGSDK.framework/TCGSDK`
- `@rpath/TTFFmpeg.framework/TTFFmpeg`
- `@rpath/TTSDKBMF.framework/TTSDKBMF`
- `@rpath/TTSDKCore.framework/TTSDKCore`
- `@rpath/TTSDKHttpDNS.framework/TTSDKHttpDNS`
- `@rpath/TTSDKLiveBase.framework/TTSDKLiveBase`
- `@rpath/TTSDKLivePlayerBMF.framework/TTSDKLivePlayerBMF`
- `@rpath/TTSDKLivePlayerNormal.framework/TTSDKLivePlayerNormal`
- `@rpath/TTSDKLivePullVolcLog.framework/TTSDKLivePullVolcLog`
- `@rpath/TTSDKPlayer.framework/TTSDKPlayer`
- `@rpath/TTSDKPlayerCoreNormal.framework/TTSDKPlayerCoreNormal`
- `@rpath/TTSDKQuicCore.framework/TTSDKQuicCore`
- `@rpath/TTSDKQuicPull.framework/TTSDKQuicPull`
- `@rpath/TTSDKReachability.framework/TTSDKReachability`
- `@rpath/TTSDKStrategyPull.framework/TTSDKStrategyPull`
- `@rpath/TTSDKTTFFmpegNormal.framework/TTSDKTTFFmpegNormal`
- `@rpath/TTSDKTools.framework/TTSDKTools`
- `@rpath/TTSDKTopSignature.framework/TTSDKTopSignature`
- `@rpath/TTSDKVCN.framework/TTSDKVCN`
- `@rpath/TTSDKVolcLog.framework/TTSDKVolcLog`
- `@rpath/TWEBRTC.framework/TWEBRTC`
- `@rpath/VolcBaseLog.framework/VolcBaseLog`
- `@rpath/VolcEngineRTC.framework/VolcEngineRTC`
- `@rpath/aosl.framework/aosl`
- `@rpath/bytenn.framework/bytenn`
- `@rpath/h265enc.framework/h265enc`
- `@rpath/libvcn.framework/libvcn`
- `@rpath/nuisdk.framework/nuisdk`
- `@rpath/ttboringssl.framework/ttboringssl`
- `@rpath/ttcrypto.framework/ttcrypto`

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

**技术栈推断**：Objective-C（__objc_* 元数据节 + ObjC 类符号）；Swift（__swift5_* 节 / Swift mangled 符号 / libswift 运行时）；C/C++（Itanium mangled 符号）；JavaScriptCore（依赖库线索）；原生编译产物（__cstring 等静态字符串节）

> 静态节名 / 符号前缀 / 依赖库路径，仅为线索，不代表运行时行为

---

本报告由只读静态解析生成，用于学习 iOS 二进制组织方式与工程实践；
不包含、也不构成对任何技术措施的规避方法。
