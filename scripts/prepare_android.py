"""Ajusta el proyecto Android que genera `npx cap add android`.
Se ejecuta en GitHub Actions justo antes de compilar."""
import os, re, pathlib

root = pathlib.Path("android")
manifest = root / "app/src/main/AndroidManifest.xml"
text = manifest.read_text(encoding="utf-8")

perms = [
    "android.permission.RECORD_AUDIO",
    "android.permission.POST_NOTIFICATIONS",
    "android.permission.RECEIVE_BOOT_COMPLETED",
    "android.permission.VIBRATE",
]
add = ""
for p in perms:
    if p not in text:
        add += f'    <uses-permission android:name="{p}" />\n'
if add:
    text = text.replace("</manifest>", add + "</manifest>")
if "android.speech.RecognitionService" not in text:
    q = ('    <queries>\n        <intent>\n'
         '            <action android:name="android.speech.RecognitionService" />\n'
         '        </intent>\n    </queries>\n')
    text = text.replace("</manifest>", q + "</manifest>")
manifest.write_text(text, encoding="utf-8")

# Número de versión creciente para poder actualizar sobre una instalación previa.
code = os.environ.get("VERSION_CODE", "1")
gradle = root / "app/build.gradle"
g = gradle.read_text(encoding="utf-8")
g = re.sub(r"versionCode\s+\d+", f"versionCode {code}", g)
g = re.sub(r'versionName\s+"[^"]*"', f'versionName "1.0.{code}"', g)
# Firma fija: siempre la misma llave (signing/debug.keystore) para que cada APK
# se instale encima del anterior sin borrar los datos.
sign = """    signingConfigs {
        debug {
            storeFile file("../../signing/debug.keystore")
            storePassword "android"
            keyAlias "androiddebugkey"
            keyPassword "android"
        }
    }
"""
if "signing/debug.keystore" not in g:
    assert "    buildTypes {" in g, "no encontré buildTypes en build.gradle"
    g = g.replace("    buildTypes {", sign + "    buildTypes {", 1)
gradle.write_text(g, encoding="utf-8")
print("Proyecto Android preparado. versionCode =", code)

# Health Connect necesita Android 8 (API 26) o superior.
var = root / "variables.gradle"
v = var.read_text(encoding="utf-8")
v = re.sub(r"minSdkVersion\s*=\s*\d+", "minSdkVersion = 26", v)
var.write_text(v, encoding="utf-8")
print("minSdkVersion = 26")
