import os, struct, zlib, shutil

# ── CONFIGURAZIONE ────────────────────────────────────────────────────
PACKAGE_NAME = "it.edu.filattiera84.app"
APP_NAME     = "IC Filattiera 84"
MIN_SDK      = 24
TARGET_SDK   = 35
COMPILE_SDK  = 35

# ── HELPER ───────────────────────────────────────────────────────────
def mkdir(p):
    if p:
        os.makedirs(p, exist_ok=True)

def write(path, content, mode="w"):
    mkdir(os.path.dirname(path))
    with open(path, mode) as f:
        f.write(content)

# ── CARTELLE ─────────────────────────────────────────────────────────
pkg_path = "app/src/main/java/" + PACKAGE_NAME.replace(".", "/")
mkdir(pkg_path)
mkdir("app/src/main/assets")
mkdir("app/src/main/res/values")
mkdir("app/src/main/res/xml")
for res in ["mipmap-hdpi","mipmap-mdpi","mipmap-xhdpi","mipmap-xxhdpi","mipmap-xxxhdpi"]:
    mkdir("app/src/main/res/" + res)

# ── COPIA index.html ─────────────────────────────────────────────────
copied = False
for candidate in [
    "filattiera84-app/src/index.html",
    "filattiera84-app/android/app/src/main/assets/index.html",
    "src/index.html",
]:
    if os.path.exists(candidate):
        shutil.copy(candidate, "app/src/main/assets/index.html")
        print("Copiato: " + candidate)
        copied = True
        break

if not copied:
    write("app/src/main/assets/index.html", """<!DOCTYPE html>
<html><head><meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>IC Filattiera 84</title>
<style>body{margin:0;background:#003366;color:white;font-family:sans-serif;
display:flex;align-items:center;justify-content:center;height:100vh;text-align:center}
a{color:#f5a623;font-size:18px;display:block;margin-top:12px}</style>
</head><body><div>
<h1>IC P.zza Filattiera 84</h1><p>Roma</p>
<a href="https://www.filattiera84.edu.it">Vai al sito ufficiale</a>
</div></body></html>""")
    print("Creato index.html di fallback")

# ── AndroidManifest.xml ───────────────────────────────────────────────
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
    <activity
      android:name=".WebViewActivity"
      android:exported="false"
      android:configChanges="orientation|screenSize"/>
  </application>
</manifest>
""")

# ── MainActivity.java ─────────────────────────────────────────────────
write(pkg_path + "/MainActivity.java", """package it.edu.filattiera84.app;
import android.app.Activity;
import android.content.Intent;
import android.os.Bundle;
import android.webkit.JavascriptInterface;
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
        webView.addJavascriptInterface(new Bridge(), "AndroidBridge");
        setContentView(webView);
        webView.loadUrl("file:///android_asset/index.html");
    }
    class Bridge {
        @JavascriptInterface
        public void openWebView(String url) {
            Intent i = new Intent(MainActivity.this, WebViewActivity.class);
            i.putExtra("url", url);
            startActivity(i);
        }
    }
    @Override
    public void onBackPressed() {
        if (webView.canGoBack()) webView.goBack();
        else super.onBackPressed();
    }
}
""")

# ── WebViewActivity.java ──────────────────────────────────────────────
write(pkg_path + "/WebViewActivity.java", """package it.edu.filattiera84.app;
import android.app.Activity;
import android.graphics.Color;
import android.graphics.Typeface;
import android.os.Bundle;
import android.view.View;
import android.webkit.WebChromeClient;
import android.webkit.WebResourceRequest;
import android.webkit.WebSettings;
import android.webkit.WebView;
import android.webkit.WebViewClient;
import android.widget.ProgressBar;
import android.widget.RelativeLayout;
import android.widget.TextView;
public class WebViewActivity extends Activity {
    private WebView webView;
    private ProgressBar progressBar;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        String url = getIntent().getStringExtra("url");
        if (url == null) url = "https://www.filattiera84.edu.it/";
        RelativeLayout layout = new RelativeLayout(this);
        layout.setBackgroundColor(Color.parseColor("#003366"));
        // Toolbar
        RelativeLayout toolbar = new RelativeLayout(this);
        toolbar.setId(View.generateViewId());
        toolbar.setBackgroundColor(Color.parseColor("#003366"));
        toolbar.setPadding(24, 48, 24, 16);
        RelativeLayout.LayoutParams tbp = new RelativeLayout.LayoutParams(
            RelativeLayout.LayoutParams.MATCH_PARENT, 150);
        tbp.addRule(RelativeLayout.ALIGN_PARENT_TOP);
        toolbar.setLayoutParams(tbp);
        // Bottone indietro
        TextView back = new TextView(this);
        back.setText("← Indietro");
        back.setTextColor(Color.WHITE);
        back.setTextSize(15);
        back.setPadding(8, 8, 32, 8);
        final WebViewActivity self = this;
        back.setOnClickListener(v -> {
            if (webView.canGoBack()) webView.goBack();
            else self.finish();
        });
        RelativeLayout.LayoutParams bp = new RelativeLayout.LayoutParams(
            RelativeLayout.LayoutParams.WRAP_CONTENT,
            RelativeLayout.LayoutParams.WRAP_CONTENT);
        bp.addRule(RelativeLayout.ALIGN_PARENT_START);
        bp.addRule(RelativeLayout.CENTER_VERTICAL);
        back.setLayoutParams(bp);
        toolbar.addView(back);
        // Titolo
        TextView title = new TextView(this);
        title.setText("IC Filattiera 84");
        title.setTextColor(Color.WHITE);
        title.setTextSize(15);
        title.setTypeface(null, Typeface.BOLD);
        RelativeLayout.LayoutParams tp = new RelativeLayout.LayoutParams(
            RelativeLayout.LayoutParams.WRAP_CONTENT,
            RelativeLayout.LayoutParams.WRAP_CONTENT);
        tp.addRule(RelativeLayout.CENTER_IN_PARENT);
        title.setLayoutParams(tp);
        toolbar.addView(title);
        layout.addView(toolbar);
        // ProgressBar
        progressBar = new ProgressBar(this, null, android.R.attr.progressBarStyleHorizontal);
        RelativeLayout.LayoutParams pbp = new RelativeLayout.LayoutParams(
            RelativeLayout.LayoutParams.MATCH_PARENT, 8);
        pbp.addRule(RelativeLayout.BELOW, toolbar.getId());
        progressBar.setLayoutParams(pbp);
        progressBar.setId(View.generateViewId());
        progressBar.setMax(100);
        layout.addView(progressBar);
        // WebView
        webView = new WebView(this);
        RelativeLayout.LayoutParams wvp = new RelativeLayout.LayoutParams(
            RelativeLayout.LayoutParams.MATCH_PARENT,
            RelativeLayout.LayoutParams.MATCH_PARENT);
        wvp.addRule(RelativeLayout.BELOW, progressBar.getId());
        webView.setLayoutParams(wvp);
        WebSettings ws = webView.getSettings();
        ws.setJavaScriptEnabled(true);
        ws.setDomStorageEnabled(true);
        ws.setLoadWithOverviewMode(true);
        ws.setUseWideViewPort(true);
        ws.setCacheMode(WebSettings.LOAD_DEFAULT);
        webView.setWebViewClient(new WebViewClient() {
            @Override
            public boolean shouldOverrideUrlLoading(WebView v, WebResourceRequest r) {
                return false;
            }
        });
        webView.setWebChromeClient(new WebChromeClient() {
            @Override
            public void onProgressChanged(WebView v, int p) {
                progressBar.setProgress(p);
                progressBar.setVisibility(p == 100 ? View.GONE : View.VISIBLE);
            }
        });
        layout.addView(webView);
        setContentView(layout);
        webView.loadUrl(url);
    }
    @Override
    public void onBackPressed() {
        if (webView.canGoBack()) webView.goBack();
        else finish();
    }
}
""")

# ── strings.xml ───────────────────────────────────────────────────────
write("app/src/main/res/values/strings.xml", """<?xml version="1.0" encoding="utf-8"?>
<resources>
    <string name="app_name">IC Filattiera 84</string>
</resources>
""")

# ── styles.xml ────────────────────────────────────────────────────────
write("app/src/main/res/values/styles.xml", """<?xml version="1.0" encoding="utf-8"?>
<resources>
    <style name="AppTheme" parent="Theme.AppCompat.Light.NoActionBar">
        <item name="colorPrimary">#003366</item>
        <item name="android:statusBarColor">#003366</item>
        <item name="android:navigationBarColor">#ffffff</item>
    </style>
</resources>
""")

# ── ICONA ─────────────────────────────────────────────────────────────
if os.path.exists("icon.png"):
    for res in ["mipmap-hdpi","mipmap-mdpi","mipmap-xhdpi","mipmap-xxhdpi","mipmap-xxxhdpi"]:
        shutil.copy("icon.png", "app/src/main/res/" + res + "/ic_launcher.png")
    print("Icona personalizzata applicata!")
else:
    def make_png(w, h, r, g, b):
        rows = []
        for _ in range(h):
            row = [0]
            for _ in range(w): row += [r, g, b, 255]
            rows.append(bytes(row))
        raw = b"".join(rows)
        def chunk(t, d):
            c = struct.pack(">I", len(d)) + t + d
            return c + struct.pack(">I", zlib.crc32(c[4:]) & 0xFFFFFFFF)
        return (b"\x89PNG\r\n\x1a\n"
                + chunk(b"IHDR", struct.pack(">IIBBBBB", w, h, 8, 6, 0, 0, 0))
                + chunk(b"IDAT", zlib.compress(raw, 9))
                + chunk(b"IEND", b""))
    for res in ["mipmap-hdpi","mipmap-mdpi","mipmap-xhdpi","mipmap-xxhdpi","mipmap-xxxhdpi"]:
        write("app/src/main/res/" + res + "/ic_launcher.png",
              make_png(192, 192, 0, 51, 102), mode="wb")
    print("Icona blu predefinita creata")

# ── settings.gradle ───────────────────────────────────────────────────
write("settings.gradle", """pluginManagement {
    repositories {
        google()
        mavenCentral()
        gradlePluginPortal()
    }
}
dependencyResolutionManagement {
    repositories {
        google()
        mavenCentral()
    }
}
rootProject.name = 'filattiera84'
include ':app'
""")

# ── build.gradle (root) ───────────────────────────────────────────────
write("build.gradle", """plugins {
    id 'com.android.application' version '8.7.0' apply false
}
""")

# ── build.gradle (app) ───────────────────────────────────────────────
write("app/build.gradle", """plugins {
    id 'com.android.application'
}
android {
    namespace 'it.edu.filattiera84.app'
    compileSdk 35
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

# ── gradle.properties ────────────────────────────────────────────────
write("gradle.properties",
      "org.gradle.jvmargs=-Xmx2048m\nandroid.useAndroidX=true\nandroid.enableJetifier=true\n")

print("✅ Progetto Android generato con successo!")
