import os, struct, zlib

def mkdir(p):
    if p:
        os.makedirs(p, exist_ok=True)

def write(path, content, mode="w"):
    mkdir(os.path.dirname(path))
    with open(path, mode) as f:
        f.write(content)

# Cartelle
mkdir("app/src/main/java/it/edu/filattiera84/app")
mkdir("app/src/main/assets")
mkdir("app/src/main/res/values")
mkdir("app/src/main/res/mipmap-hdpi")

# Copia index.html se esiste, altrimenti crea fallback
src = None
for candidate in [
    "filattiera84-app/src/index.html",
    "filattiera84-app/android/app/src/main/assets/index.html",
]:
    if os.path.exists(candidate):
        src = candidate
        break

if src:
    with open(src) as f:
        content = f.read()
    write("app/src/main/assets/index.html", content)
    print(f"Copiato: {src}")
else:
    write("app/src/main/assets/index.html", """<!DOCTYPE html>
<html><head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>IC Filattiera 84</title>
<style>
body{margin:0;background:#003366;color:white;font-family:sans-serif;
display:flex;align-items:center;justify-content:center;height:100vh;text-align:center}
a{color:#f5a623;font-size:18px}
</style>
</head><body>
<div>
  <h1>IC P.zza Filattiera 84</h1>
  <p>Roma</p>
  <a href="https://www.filattiera84.edu.it">Vai al sito ufficiale</a>
</div>
</body></html>""")
    print("Creato index.html di fallback")

# AndroidManifest.xml
write("app/src/main/AndroidManifest.xml", """<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android">
  <uses-permission android:name="android.permission.INTERNET"/>
  <uses-permission android:name="android.permission.ACCESS_NETWORK_STATE"/>
  <application
    android:allowBackup="true"
    android:icon="@mipmap/ic_launcher"
    android:label="@string/app_name"
    android:theme="@style/AppTheme">
    <activity
      android:name=".MainActivity"
      android:exported="true"
      android:configChanges="orientation|screenSize">
      <intent-filter>
        <action android:name="android.intent.action.MAIN"/>
        <category android:name="android.intent.category.LAUNCHER"/>
      </intent-filter>
    </activity>
  </application>
</manifest>
""")

# MainActivity.java
write("app/src/main/java/it/edu/filattiera84/app/MainActivity.java", """package it.edu.filattiera84.app;
import android.app.Activity;
import android.os.Bundle;
import android.webkit.WebSettings;
import android.webkit.WebView;
import android.webkit.WebViewClient;
public class MainActivity extends Activity {
    private WebView webView;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        webView = new WebView(this);
        WebSettings s = webView.getSettings();
        s.setJavaScriptEnabled(true);
        s.setDomStorageEnabled(true);
        s.setAllowFileAccessFromFileURLs(true);
        s.setAllowUniversalAccessFromFileURLs(true);
        webView.setWebViewClient(new WebViewClient());
        setContentView(webView);
        webView.loadUrl("file:///android_asset/index.html");
    }
    @Override
    public void onBackPressed() {
        if (webView.canGoBack()) webView.goBack();
        else super.onBackPressed();
    }
}
""")

# strings.xml
write("app/src/main/res/values/strings.xml", """<?xml version="1.0" encoding="utf-8"?>
<resources>
    <string name="app_name">IC Filattiera 84</string>
</resources>
""")

# styles.xml
write("app/src/main/res/values/styles.xml", """<?xml version="1.0" encoding="utf-8"?>
<resources>
    <style name="AppTheme" parent="Theme.AppCompat.Light.NoActionBar">
        <item name="colorPrimary">#003366</item>
        <item name="android:statusBarColor">#003366</item>
    </style>
</resources>
""")

# Icona da file caricato nel repository
import shutil
if os.path.exists('icon.png'):
    for res in ['mipmap-hdpi','mipmap-mdpi','mipmap-xhdpi','mipmap-xxhdpi','mipmap-xxxhdpi']:
        mkdir('app/src/main/res/'+res)
        shutil.copy('icon.png','app/src/main/res/'+res+'/ic_launcher.png')
    print("Icona personalizzata applicata!")
else:
    print("ATTENZIONE: icon.png non trovato, uso icona predefinita")
    def make_png(w,h,r,g,b):
        rows=[]
        for _ in range(h):
            row=[0]
            for _ in range(w): row+=[r,g,b,255]
            rows.append(bytes(row))
        raw=b"".join(rows)
        def chunk(t,d):
            c=struct.pack(">I",len(d))+t+d
            return c+struct.pack(">I",zlib.crc32(c[4:])&0xFFFFFFFF)
        return(b"\x89PNG\r\n\x1a\n"
            +chunk(b"IHDR",struct.pack(">IIBBBBB",w,h,8,6,0,0,0))
            +chunk(b"IDAT",zlib.compress(raw,9))
            +chunk(b"IEND",b""))
    for res in ['mipmap-hdpi','mipmap-mdpi','mipmap-xhdpi','mipmap-xxhdpi','mipmap-xxxhdpi']:
        mkdir('app/src/main/res/'+res)
        write('app/src/main/res/'+res+'/ic_launcher.png',
              make_png(192,192,0,51,102),mode="wb")

# build.gradle (app)
write("app/build.gradle", """plugins { id 'com.android.application' }
android {
    namespace 'it.edu.filattiera84.app'
  compileSdk 35
    buildToolsVersion "35.0.0"
    defaultConfig {
        applicationId "it.edu.filattiera84.app"
        minSdk 24
        targetSdk 35
        versionCode 1
        versionName "1.0"
    }
    compileOptions {
        sourceCompatibility JavaVersion.VERSION_17
        targetCompatibility JavaVersion.VERSION_17
    }
}
dependencies {
    implementation 'androidx.appcompat:appcompat:1.6.1'
    implementation 'androidx.webkit:webkit:1.9.0'
}
""")

# build.gradle (root)
write("build.gradle", """buildscript {
    repositories { google(); mavenCentral() }
    dependencies { classpath 'com.android.tools.build:gradle:8.7.0' }
}
allprojects { repositories { google(); mavenCentral() } }
""")

# settings.gradle
write("settings.gradle", "rootProject.name = 'filattiera84'\ninclude ':app'\n")

# gradle.properties
write("gradle.properties",
      "org.gradle.jvmargs=-Xmx2048m\nandroid.useAndroidX=true\nandroid.enableJetifier=true\n")

print("Progetto Android generato con successo!")
