# 📱 Come ottenere l'APK tramite GitHub Actions
## Guida passo passo — nessun software da installare

---

## FASE 1 — Crea account GitHub (se non ce l'hai)

1. Vai su **https://github.com**
2. Clicca **Sign up** → inserisci email, password, username
3. Conferma l'email

---

## FASE 2 — Crea il repository

1. Dopo il login, clicca il **+** in alto a destra → **New repository**
2. Inserisci:
   - **Repository name:** `filattiera84-app`
   - Visibilità: **Public** ✅ (necessario per Actions gratuiti)
   - NON spuntare "Add README"
3. Clicca **Create repository**

---

## FASE 3 — Carica i file del progetto

### Metodo A — Caricamento drag & drop (il più semplice)

1. Nella pagina del repository appena creato, clicca **uploading an existing file**
2. Estrai lo zip `filattiera84-app.zip` sul tuo computer
3. **Trascina l'intera cartella `filattiera84-app`** nella pagina GitHub
4. Scrivi un messaggio di commit, es: `Prima versione app`
5. Clicca **Commit changes**

### Metodo B — Da terminale (se hai Git installato)

```bash
cd filattiera84-app
git init
git add .
git commit -m "Prima versione app"
git branch -M main
git remote add origin https://github.com/TUO_USERNAME/filattiera84-app.git
git push -u origin main
```

---

## FASE 4 — Avvia la build (automatica o manuale)

La build **parte automaticamente** a ogni push. Oppure:

1. Vai nel tab **Actions** del repository
2. Clicca su **Build APK — IC Filattiera 84** (nella lista a sinistra)
3. Clicca **Run workflow** → **Run workflow** (bottone verde)
4. ⏳ Attendi 5-8 minuti

---

## FASE 5 — Scarica l'APK ✅

1. Nel tab **Actions** clicca sull'ultima build riuscita (icona ✅ verde)
2. Scorri in basso fino alla sezione **Artifacts**
3. Clicca su **filattiera84-debug-apk**
4. Si scarica uno zip → estrailo → dentro c'è **app-debug.apk**

---

## FASE 6 — Installa l'APK sul telefono Android

1. Copia `app-debug.apk` sul telefono (via USB, email, WhatsApp, Drive…)
2. Sul telefono: **Impostazioni → Sicurezza → Origini sconosciute** → attiva
3. Apri il file APK con il gestore file
4. Clicca **Installa**

> Per Android 8+: la prima volta che apri il file, il sistema chiede
> di autorizzare l'installazione dall'app che hai usato per aprirlo
> (es. Chrome o il gestore file). Autorizza e poi reinstalla.

---

## Note importanti

| ℹ️ | Dettaglio |
|----|-----------|
| **Tipo APK** | Debug (installabile direttamente, non pubblicabile su Play Store) |
| **Per Play Store** | Serve firma release — contatta un tecnico o usa Android Studio |
| **Aggiornamenti** | Ogni volta che modifichi il codice e fai push, Actions ricompila automaticamente |
| **Scadenza artefatto** | L'APK resta disponibile per **30 giorni** su GitHub |
| **Versione minima Android** | Android 7.0 (API 24) e superiori |

---

## Struttura del progetto caricato

```
filattiera84-app/
├── .github/
│   └── workflows/
│       └── build-apk.yml        ← istruzioni per GitHub Actions
├── android/
│   ├── app/
│   │   ├── src/main/
│   │   │   ├── AndroidManifest.xml
│   │   │   ├── assets/          ← app web (index.html)
│   │   │   ├── java/it/edu/filattiera84/app/
│   │   │   │   └── MainActivity.java
│   │   │   └── res/             ← icone, stili, temi
│   │   └── build.gradle
│   ├── build.gradle
│   ├── settings.gradle
│   └── gradlew
├── src/
│   └── index.html               ← app web principale
├── capacitor.config.json
├── package.json
└── README.md
```
