[app]
# ऐप का नाम और सेटिंग्स
title = Cyber Launcher
package.name = cyberlauncher
package.domain = org.test
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 0.1

# सबसे जरूरी लाइन (इसे सिंपल रखा है)
requirements = python3,kivy==2.2.0

# स्क्रीन सेटिंग्स
orientation = portrait
fullscreen = 0
android.permissions = INTERNET

# Android वर्जन (इसे थोड़ा कम किया है ताकि एरर न आए)
android.api = 31
android.minapi = 21
android.accept_sdk_license = True
android.archs = arm64-v8a

# यह है असली फिक्स (Master की जगह Stable)
p4a.branch = stable

[buildozer]
log_level = 2
warn_on_root = 1
