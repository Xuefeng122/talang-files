#import <Foundation/Foundation.h>

NS_ASSUME_NONNULL_BEGIN

/// 只读的本地偏好访问层。所有状态都存放在宿主进程自己的偏好域里，
/// 不读取、不改写宿主 App 的任何业务数据。
@interface RKSettings : NSObject

+ (NSDictionary *)prefs;
+ (BOOL)isEnabled;
+ (void)setEnabled:(BOOL)enabled;
+ (BOOL)loggingEnabled;
+ (void)setLoggingEnabled:(BOOL)enabled;

/// 只有被显式列进 AllowedBundleIdentifiers 的进程才会安装钩子与显示面板。
+ (BOOL)shouldAttachToBundleIdentifier:(NSString *)identifier;
+ (NSString *)panelTitle;
+ (void)log:(NSString *)format, ... NS_FORMAT_FUNCTION(1, 2);

@end

NS_ASSUME_NONNULL_END
