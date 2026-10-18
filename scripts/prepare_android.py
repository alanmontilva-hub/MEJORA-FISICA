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
gradle.write_text(g, encoding="utf-8")
print("Proyecto Android preparado. versionCode =", code)
