#import "RKSettings.h"
#include <stdarg.h>

static NSString *const kRKPreferencesKey = @"ResearchKitPrefs";

@implementation RKSettings

+ (NSMutableDictionary *)mutablePrefs {
    NSDictionary *saved = [[NSUserDefaults standardUserDefaults] dictionaryForKey:kRKPreferencesKey];
    if ([saved isKindOfClass:[NSDictionary class]]) {
        return [saved mutableCopy];
    }
    NSDictionary *bundled = [[NSBundle mainBundle] objectForInfoDictionaryKey:@"ResearchKitDefaults"];
    if ([bundled isKindOfClass:[NSDictionary class]]) {
        return [bundled mutableCopy];
    }
    return [NSMutableDictionary dictionary];
}

+ (NSDictionary *)prefs {
    return [self mutablePrefs];
}

+ (void)setBoolValue:(BOOL)value forKey:(NSString *)key {
    NSMutableDictionary *prefs = [self mutablePrefs];
    prefs[key] = @(value);
    [[NSUserDefaults standardUserDefaults] setObject:prefs forKey:kRKPreferencesKey];
}

+ (BOOL)boolForKey:(NSString *)key fallback:(BOOL)fallback {
    id value = [self prefs][key];
    return [value isKindOfClass:[NSNumber class]] ? [value boolValue] : fallback;
}

+ (BOOL)isEnabled {
    return [self boolForKey:@"Enabled" fallback:NO];
}

+ (void)setEnabled:(BOOL)enabled {
    [self setBoolValue:enabled forKey:@"Enabled"];
}

+ (BOOL)loggingEnabled {
    return [self boolForKey:@"Logging" fallback:NO];
}

+ (void)setLoggingEnabled:(BOOL)enabled {
    [self setBoolValue:enabled forKey:@"Logging"];
}

+ (BOOL)shouldAttachToBundleIdentifier:(NSString *)identifier {
    if (identifier.length == 0) return NO;
    id allowed = [self prefs][@"AllowedBundleIdentifiers"];
    if (![allowed isKindOfClass:[NSArray class]]) return NO;
    return [(NSArray *)allowed containsObject:identifier];
}

+ (NSString *)panelTitle {
    id title = [self prefs][@"PanelTitle"];
    return [title isKindOfClass:[NSString class]] ? title : @"ResearchKit";
}

+ (void)log:(NSString *)format, ... {
    if (![self loggingEnabled]) return;
    va_list arguments;
    va_start(arguments, format);
    NSString *message = [[NSString alloc] initWithFormat:format arguments:arguments];
    va_end(arguments);
    NSLog(@"[ResearchKit] %@", message);
}

@end
