[app]

title = ClickFlow Pro Max
package.name = clickflowpromax
package.domain = com.alsofi.promax

source.dir = .
source.include_exts = py,png,jpg,kv

version = 3.0

requirements = python3,kivy,kivymd,pyjnius

orientation = portrait
fullscreen = 0

android.api = 33
android.minapi = 21

android.permissions = INTERNET

android.arch = armeabi-v7a
android.release_artifact = aab

[buildozer]
log_level = 2
warn_on_root = 1
