# 📱 App IC P.zza Filattiera 84 — Guida alla compilazione APK

## Requisiti
- **Node.js** v18+ → https://nodejs.org
- **Android Studio** (con SDK Android 33+) → https://developer.android.com/studio
- **Java JDK 17** → già incluso in Android Studio
- **Account Google Play Developer** → https://play.google.com/console

---

## 1. Installazione dipendenze

```bash
cd filattiera84-app
npm install
```

---

## 2. Aggiungere la piattaforma Android

```bash
npx cap add android
npx cap sync
```

---

## 3. Aprire in Android Studio

```bash
npx cap open android
```

Android Studio si aprirà automaticamente con il progetto.

---

## 4. Configurare Google Services (per Push Notifications)

1. Vai su https://console.firebase.google.com
2. Crea un nuovo progetto → "filattiera84-app"
3. Aggiungi app Android con package: `it.edu.filattiera84.app`
4. Scarica il file `google-services.json`
5. Copialo in: `android/app/google-services.json`

---

## 5. Creare la chiave di firma (release)

```bash
keytool -genkey -v \
  -keystore android/release-key.jks \
  -alias filattiera84 \
  -keyalg RSA -keysize 2048 \
  -validity 10000
```

⚠️ **CONSERVARE LA CHIAVE!** Senza di essa non si possono pubblicare aggiornamenti.

---

## 6. Configurare la firma in Android Studio

Apri `android/app/build.gradle` e aggiungi in `android { ... }`:

```groovy
signingConfigs {
    release {
        storeFile file("../release-key.jks")
        storePassword "TUA_PASSWORD"
        keyAlias "filattiera84"
        keyPassword "TUA_PASSWORD"
    }
}
buildTypes {
    release {
        signingConfig signingConfigs.release
        minifyEnabled false
    }
}
```

---

## 7. Generare l'APK / AAB

### APK (installazione diretta):
In Android Studio → **Build → Build Bundle(s)/APK(s) → Build APK(s)**
File output: `android/app/build/outputs/apk/release/app-release.apk`

### AAB (per Google Play — consigliato):
In Android Studio → **Build → Generate Signed Bundle/APK → Android App Bundle**
File output: `android/app/build/outputs/bundle/release/app-release.aab`

---

## 8. Pubblicare su Google Play

1. Vai su https://play.google.com/console
2. Crea nuova app → "IC P.zza Filattiera 84"
3. Carica il file `.aab`
4. Compila le informazioni richieste:
   - Categoria: **Istruzione**
   - Pubblico target: famiglie + docenti
5. Pubblica sulla traccia **Produzione** o **Test interno** prima

---

## Aggiornare i dati dell'app

I dati circolari/eventi sono nel file `src/index.html` nella sezione `DATI DEMO`.
Per un'app live, si può collegare a:

- **WordPress REST API** del sito filattiera84.edu.it
  ```
  GET https://www.filattiera84.edu.it/wp-json/wp/v2/posts?categories=circolari
  ```
- **Google Sheets** come database semplice
- **Firebase Firestore** per dati in tempo reale

---

## Struttura del progetto

```
filattiera84-app/
├── src/
│   └── index.html          ← App principale (HTML/CSS/JS)
├── capacitor.config.json   ← Config Capacitor
├── package.json
├── README.md
└── android/                ← generato da: npx cap add android
    ├── app/
    │   ├── google-services.json  ← da Firebase
    │   └── build.gradle
    └── ...
```

---

## Supporto

Per assistenza tecnica: info@saneb.care
Sito scuola: https://www.filattiera84.edu.it/
