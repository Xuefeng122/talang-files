#import <UIKit/UIKit.h>

NS_ASSUME_NONNULL_BEGIN

/// 纯本地的界面研究面板：展示宿主环境信息、两个开关与一段用途说明。
/// 它不调用宿主 App 的任何私有 API，也不参与任何业务流程。
@interface RKPanel : UIView

- (instancetype)initWithHostBundleIdentifier:(NSString *)identifier;
- (void)showInWindow:(UIWindow *)window;
- (void)dismiss;

@end

NS_ASSUME_NONNULL_END
