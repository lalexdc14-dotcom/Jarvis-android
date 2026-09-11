[app]
title = JARVIS OS
package.name = jarvisos
package.domain = org.jarvis
source.dir = .
source.include_exts = py,png,jpg,jpeg,kv,atlas
version = 5.0
requirements = python3,kivy,pyjnius
orientation = portrait
fullscreen = 0
# Si subes background.jpg al repo, descomenta la siguiente línea para usarlo como ícono:
# icon.filename = %(source.dir)s/background.jpg

[buildozer]
log_level = 2
warn_on_root = 1

android.permissions = INTERNET
android.api = 33
android.minapi = 21
android.ndk = 25b
android.accept_sdk_license = True
android.archs = arm64-v8a, armeabi-v7a
