// ResearchKit — Logos 教学模板
// 全部钩子都作用在 iOS 系统类 UIViewController 上，仅用于挂载一个本地面板。
// 不 hook 任何第三方业务类，不改写任何返回值，不触及消息、媒体、付费或广告路径。

%config(generator=MobileSubstrate)

#import <UIKit/UIKit.h>
#import "RKPanel.h"
#import "RKSettings.h"

// 为 %property 生成的方法补齐编译期声明，保证括号消息语法有类型检查。
@interface UIViewController (ResearchKitPanel)
@property (nonatomic, strong) UIView *rk_panel;
@end

%group ResearchKitGroup

%hook UIViewController

%property (nonatomic, strong) UIView *rk_panel;

- (void)viewDidAppear:(BOOL)animated {
    %orig;

    NSString *bundleID = [[NSBundle mainBundle] bundleIdentifier];
    if (![RKSettings shouldAttachToBundleIdentifier:bundleID]) return;
    if (![RKSettings isEnabled]) return;
    if ([self rk_panel]) return;

    UIWindow *window = self.view.window;
    if (!window) return;

    RKPanel *panel = [[RKPanel alloc] initWithHostBundleIdentifier:bundleID];
    [panel showInWindow:window];
    [self setRk_panel:panel];
    [RKSettings log:@"attached in %@ / %@", bundleID, NSStringFromClass([self class])];
}

%new(v@:@)
- (void)rk_dismissResearchPanel:(id)sender {
    UIView *panel = [self rk_panel];
    if ([panel isKindOfClass:[RKPanel class]]) {
        [(RKPanel *)panel dismiss];
    }
    [self setRk_panel:nil];
}

%end

%end

%ctor {
    // 分组钩子只有在显式白名单内才安装；默认不注入任何进程。
    NSString *bundleID = [[NSBundle mainBundle] bundleIdentifier];
    if ([RKSettings shouldAttachToBundleIdentifier:bundleID]) {
        %init(ResearchKitGroup);
    }
}
