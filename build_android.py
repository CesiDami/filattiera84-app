import os, struct, zlib

def mkdir(p):
    if p:
        os.makedirs(p, exist_ok=True)

def write(path, content, mode="w"):
    mkdir(os.path.dirname(path))
    with open(path, mode) as f:
        f.write(content)
# 1. LAYOUT XML (WebView + ProgressBar)
layout_content = """<?xml version="1.0" encoding="utf-8"?>
<RelativeLayout xmlns:android="http://schemas.android.com/apk/res/android"
    android:layout_width="match_parent"
    android:layout_height="match_parent">

    <WebView
        android:id="@+id/webview"
        android:layout_width="match_parent"
        android:layout_height="match_parent" />

    <ProgressBar
        android:id="@+id/progressBar"
        style="?android:attr/progressBarStyleHorizontal"
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:layout_alignParentTop="true"
        android:indeterminate="true"
        android:visibility="gone" />
</RelativeLayout>
"""

# 2. MAIN ACTIVITY (Logica Caricamento)
java_content = f"""package {PACKAGE_NAME};
import android.content.Intent;
import android.graphics.Bitmap;
import android.net.Uri;
import android.os.Bundle;
import android.view.View;
import android.webkit.WebSettings;
import android.webkit.WebView;
import android.webkit.WebViewClient;
import android.widget.ProgressBar;
import androidx.appcompat.app.AppCompatActivity;

public class MainActivity extends AppCompatActivity {{
    private WebView webView;
    private ProgressBar progressBar;

    @Override
    protected void onCreate(Bundle savedInstanceState) {{
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        webView = findViewById(R.id.webview);
        progressBar = findViewById(R.id.progressBar);

        WebSettings settings = webView.getSettings();
        settings.setJavaScriptEnabled(true);
        settings.setDomStorageEnabled(true);
        settings.setSupportZoom(true);
        settings.setBuiltInZoomControls(true);
        settings.setDisplayZoomControls(false);

        webView.setWebViewClient(new WebViewClient() {{
            @Override
            public void onPageStarted(WebView view, String url, Bitmap favicon) {{
                super.onPageStarted(view, url, favicon);
                progressBar.setVisibility(View.VISIBLE); // Mostra barra
            }}

            @Override
            public void onPageFinished(WebView view, String url) {{
                super.onPageFinished(view, url);
                progressBar.setVisibility(View.GONE); // Nascondi barra
            }}

            @Override
            public boolean shouldOverrideUrlLoading(WebView view, String url) {{
                if (url.contains("filattiera84.edu.it") || url.contains("axioscloud.it")) {{
                    view.loadUrl(url);
                    return false;
                }}
                Intent intent = new Intent(Intent.ACTION_VIEW, Uri.parse(url));
                startActivity(intent);
                return true;
            }}
        }});

        webView.loadUrl("{MAIN_URL}");
    }}

    @Override
    public void onBackPressed() {{
        if (webView.canGoBack()) {{
            webView.goBack();
        }} else {{
            super.onBackPressed();
        }}
    }}
}}
"""

# 3. MANIFEST E GRADLE (Invariati ma necessari)
manifest_content = f"""<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android" package="{PACKAGE_NAME}">
    <uses-permission android:name="android.permission.INTERNET" />
    <uses-permission android:name="android.permission.ACCESS_NETWORK_STATE" />
    <application android:label="{APP_NAME}" android:theme="@style/Theme.AppCompat.Light.NoActionBar" android:usesCleartextTraffic="true">
        <activity android:name=".MainActivity" android:exported="true" android:configChanges="orientation|screenSize">
            <intent-filter>
                <action android:name="android.intent.action.MAIN" />
                <category android:name="android.intent.category.LAUNCHER" />
            </intent-filter>
        </activity>
    </application>
</manifest>
"""

build_gradle = """
plugins { id 'com.android.application' }
android {
    namespace 'it.edu.filattiera84.app'
    compileSdk 34
    defaultConfig { applicationId "it.edu.filattiera84.app"; minSdk 24; targetSdk 34; versionCode 1; versionName "1.0" }
}
dependencies { implementation 'androidx.appcompat:appcompat:1.6.1'; implementation 'com.google.android.material:material:1.9.0' }
"""

# Esecuzione
create_structure()
write_file("app/src/main/res/layout/activity_main.xml", layout_content)
write_file("app/src/main/AndroidManifest.xml", manifest_content)
write_file("app/src/main/java/it/edu/filattiera84/app/MainActivity.java", java_content)
# build.gradle (root)
# build.gradle (app)
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
write_file("build.gradle", "buildscript { repositories { google(); mavenCentral() } dependencies { classpath 'com.android.tools.build:gradle:8.2.2' } } allprojects { repositories { google(); mavenCentral() } }")

print("Progetto aggiornato con Barra di Caricamento!")
