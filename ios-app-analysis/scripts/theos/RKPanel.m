#import "RKPanel.h"
#import "RKSettings.h"
#import <QuartzCore/QuartzCore.h>

@interface RKPanel ()
@property (nonatomic, strong) UIVisualEffectView *backdrop;
@property (nonatomic, strong) UISwitch *enableSwitch;
@property (nonatomic, strong) UISwitch *logSwitch;
@end

@implementation RKPanel

- (instancetype)initWithHostBundleIdentifier:(NSString *)identifier {
    self = [super initWithFrame:CGRectMake(0, 0, 300, 320)];
    if (!self) return nil;

    self.backgroundColor = [UIColor clearColor];
    self.layer.cornerRadius = 18.0;
    self.layer.masksToBounds = YES;
    self.layer.borderColor = [[UIColor tertiaryLabelColor] CGColor];
    self.layer.borderWidth = 0.5;
    self.autoresizingMask = UIViewAutoresizingFlexibleLeftMargin |
                            UIViewAutoresizingFlexibleRightMargin |
                            UIViewAutoresizingFlexibleTopMargin |
                            UIViewAutoresizingFlexibleBottomMargin;

    UIBlurEffect *effect = [UIBlurEffect effectWithStyle:UIBlurEffectStyleSystemMaterial];
    _backdrop = [[UIVisualEffectView alloc] initWithEffect:effect];
    _backdrop.frame = self.bounds;
    _backdrop.autoresizingMask = UIViewAutoresizingFlexibleWidth | UIViewAutoresizingFlexibleHeight;
    [self addSubview:_backdrop];

    UIView *content = _backdrop.contentView;

    UILabel *title = [[UILabel alloc] initWithFrame:CGRectMake(20, 16, 210, 28)];
    title.text = [RKSettings panelTitle];
    title.font = [UIFont boldSystemFontOfSize:18.0];
    title.textColor = [UIColor labelColor];
    [content addSubview:title];

    UIButton *close = [UIButton buttonWithType:UIButtonTypeSystem];
    close.frame = CGRectMake(250, 14, 34, 32);
    [close setTitle:@"X" forState:UIControlStateNormal];
    close.titleLabel.font = [UIFont systemFontOfSize:16.0 weight:UIFontWeightSemibold];
    [close addTarget:self action:@selector(rk_closeTapped:) forControlEvents:UIControlEventTouchUpInside];
    [content addSubview:close];

    NSString *hostVersion = [[[NSBundle mainBundle] infoDictionary] objectForKey:@"CFBundleShortVersionString"] ?: @"-";
    UILabel *info = [[UILabel alloc] initWithFrame:CGRectMake(20, 50, 260, 64)];
    info.numberOfLines = 0;
    info.font = [UIFont monospacedSystemFontOfSize:11.0 weight:UIFontWeightRegular];
    info.textColor = [UIColor secondaryLabelColor];
    info.text = [NSString stringWithFormat:@"Host  %@ (%@)\niOS   %@   Panel 0.1.0\nLocal UI only - no business hooks",
                 identifier, hostVersion, [[UIDevice currentDevice] systemVersion]];
    [content addSubview:info];

    UIView *line = [[UIView alloc] initWithFrame:CGRectMake(20, 124, 260, 0.5)];
    line.backgroundColor = [UIColor separatorColor];
    [content addSubview:line];

    UILabel *enableTitle = [[UILabel alloc] initWithFrame:CGRectMake(20, 138, 190, 31)];
    enableTitle.text = @"Enable panel";
    enableTitle.font = [UIFont systemFontOfSize:14.0];
    enableTitle.textColor = [UIColor labelColor];
    [content addSubview:enableTitle];

    _enableSwitch = [[UISwitch alloc] initWithFrame:CGRectZero];
    _enableSwitch.frame = CGRectMake(238, 138, 51, 31);
    [_enableSwitch setOn:[RKSettings isEnabled] animated:NO];
    [_enableSwitch addTarget:self action:@selector(rk_enableChanged:) forControlEvents:UIControlEventValueChanged];
    [content addSubview:_enableSwitch];

    UILabel *logTitle = [[UILabel alloc] initWithFrame:CGRectMake(20, 180, 190, 31)];
    logTitle.text = @"Debug logging";
    logTitle.font = [UIFont systemFontOfSize:14.0];
    logTitle.textColor = [UIColor labelColor];
    [content addSubview:logTitle];

    _logSwitch = [[UISwitch alloc] initWithFrame:CGRectZero];
    _logSwitch.frame = CGRectMake(238, 180, 51, 31);
    [_logSwitch setOn:[RKSettings loggingEnabled] animated:NO];
    [_logSwitch addTarget:self action:@selector(rk_logChanged:) forControlEvents:UIControlEventValueChanged];
    [content addSubview:_logSwitch];

    UILabel *note = [[UILabel alloc] initWithFrame:CGRectMake(20, 226, 260, 78)];
    note.numberOfLines = 0;
    note.font = [UIFont systemFontOfSize:11.0];
    note.textColor = [UIColor tertiaryLabelColor];
    note.text = @"Teaching template for Logos directives, preference handling and in-app UI overlay. It does not read, alter or forward any user content or app business data.";
    [content addSubview:note];

    return self;
}

- (void)showInWindow:(UIWindow *)window {
    if (self.superview) return;
    self.center = CGPointMake(CGRectGetMidX(window.bounds), CGRectGetMidY(window.bounds));
    self.alpha = 0.0;
    self.transform = CGAffineTransformMakeScale(0.94, 0.94);
    [window addSubview:self];
    [UIView animateWithDuration:0.22
                          delay:0
                        options:UIViewAnimationOptionCurveEaseOut
                     animations:^{
                         self.alpha = 1.0;
                         self.transform = CGAffineTransformIdentity;
                     }
                     completion:nil];
}

- (void)dismiss {
    [UIView animateWithDuration:0.18
                     animations:^{ self.alpha = 0.0; }
                     completion:^(BOOL finished) { [self removeFromSuperview]; }];
}

- (void)rk_enableChanged:(UISwitch *)sender {
    [RKSettings setEnabled:sender.isOn];
    [RKSettings log:@"panel enabled = %@", sender.isOn ? @"YES" : @"NO"];
}

- (void)rk_logChanged:(UISwitch *)sender {
    [RKSettings setLoggingEnabled:sender.isOn];
    if (sender.isOn) [RKSettings log:@"debug logging enabled"];
}

- (void)rk_closeTapped:(id)sender {
    [RKSettings log:@"panel dismissed by user"];
    [self dismiss];
}

@end
