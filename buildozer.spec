[app]
title = CDJ Simulator
package.name = cdjsim
package.domain = org.example
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 0.1
requirements = python3,kivy,kivymd,plyer
orientation = portrait

[android]
fullscreen = 0
# Permissions
android.permissions = ReadExternalStorage,WriteExternalStorage

[buildozer]
log_level = 2
warn_on_root = 1
