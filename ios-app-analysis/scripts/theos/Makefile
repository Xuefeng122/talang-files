# ResearchKit — 本地 UI 研究模板（教学用途）
# 不含任何修改第三方 App 业务逻辑、付费、广告、水印或消息处理的代码。
THEOS ?= /c/theos/theos

export TARGET := iphone:clang:16.5:16.0
export ARCHS := arm64 arm64e
export DEBUG := 0

include $(THEOS)/makefiles/common.mk

TWEAK_NAME := ResearchKit
ResearchKit_FILES := Tweak.x RKPanel.m RKSettings.m
ResearchKit_FRAMEWORKS := UIKit Foundation CoreGraphics QuartzCore
ResearchKit_CFLAGS := -fobjc-arc -Wno-deprecated-declarations

include $(THEOS_MAKE_PATH)/tweak.mk

after-stage::
	@echo "ResearchKit staged (local UI template only)"
