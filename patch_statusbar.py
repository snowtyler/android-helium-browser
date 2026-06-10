import os
import sys

file_path = 'chrome/android/java/src/org/chromium/chrome/browser/ui/system/StatusBarColorController.java'
if not os.path.exists(file_path):
    print(f"Error: {file_path} does not exist.")
    sys.exit(1)

with open(file_path, 'rb') as f:
    raw_content = f.read()

content = raw_content.decode('utf-8').replace('\r\n', '\n')

old_update = """    public void updateStatusBarColor() {
        @ColorInt int statusBarColor = calculateFinalStatusBarColor();
        setStatusBarColor(
                mEdgeToEdgeSystemBarColorHelper,
                mActivity,
                statusBarColor,
                mForceLightIconColorForNtp && isStandardNtp() && !mIsOmniboxFocused);"""

new_update = """    public void updateStatusBarColor() {
        @ColorInt int statusBarColor = calculateFinalStatusBarColor();
        boolean isBottomBar = mBrowserControlsStateProvider.getControlsPosition() == ControlsPosition.BOTTOM;
        if (isBottomBar) {
            setStatusBarColor(
                    mEdgeToEdgeSystemBarColorHelper,
                    mActivity,
                    Color.TRANSPARENT,
                    statusBarColor,
                    mForceLightIconColorForNtp && isStandardNtp() && !mIsOmniboxFocused);
        } else {
            setStatusBarColor(
                    mEdgeToEdgeSystemBarColorHelper,
                    mActivity,
                    statusBarColor,
                    mForceLightIconColorForNtp && isStandardNtp() && !mIsOmniboxFocused);
        }"""

if old_update in content:
    content = content.replace(old_update, new_update)
    print("Successfully replaced updateStatusBarColor")
else:
    print("Error: old_update pattern not found exactly.")
    sys.exit(1)

target_block = """    public static void setStatusBarColor(
            @Nullable EdgeToEdgeSystemBarColorHelper edgeToEdgeSystemBarColorHelper,
            Activity activity,
            @ColorInt int color,
            boolean forceLightIconColor) {"""

new_set_code = """    public static void setStatusBarColor(
            @Nullable EdgeToEdgeSystemBarColorHelper edgeToEdgeSystemBarColorHelper,
            Activity activity,
            @ColorInt int color,
            boolean forceLightIconColor) {
        setStatusBarColor(edgeToEdgeSystemBarColorHelper, activity, color, color, forceLightIconColor);
    }

    public static void setStatusBarColor(
            @Nullable EdgeToEdgeSystemBarColorHelper edgeToEdgeSystemBarColorHelper,
            Activity activity,
            @ColorInt int color,
            @ColorInt int iconContrastColor,
            boolean forceLightIconColor) {"""

if target_block in content:
    content = content.replace(target_block, new_set_code)
    
    original_body_start = "        boolean needsDarkStatusBarIcons = !ColorUtils.shouldUseLightForegroundOnBackground(color);"
    new_body_start = "        boolean needsDarkStatusBarIcons = !ColorUtils.shouldUseLightForegroundOnBackground(iconContrastColor);"
    content = content.replace(original_body_start, new_body_start)
    
    original_opaque = "        @ColorInt int opaqueColor = ColorUtils.getOpaqueColor(color);"
    new_opaque = "        @ColorInt int opaqueColor = ColorUtils.getOpaqueColor(iconContrastColor);"
    content = content.replace(original_opaque, new_opaque)
    
    print("Successfully replaced setStatusBarColor definition")
else:
    print("Error: target_block not found.")
    sys.exit(1)

with open(file_path, 'wb') as f:
    f.write(content.encode('utf-8'))
