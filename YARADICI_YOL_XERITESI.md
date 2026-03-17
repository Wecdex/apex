# APEX Userbot - Yaradici Yol Xeritesi

## 1. LAYIHE ANALIZI - TAPILAN PROBLEMLER

### 1.1 KRITIK BUGLAR (Bot islemesine mane olur)

| # | Fayl | Problem | Status |
|---|------|---------|--------|
| 1 | `events.py:120` | `remove("error.log")` yazilir amma fayl `ΣRROR.log` adinda yaradilir. Crash edir. | DUZELDILECEK |
| 2 | `__init__.py:11` | `distutils.util.strtobool` Python 3.12-de deprecated, 3.13-de silinib. | DUZELDILECEK |
| 3 | `events.py:109` | `open("ΣRROR.log", "w+")` encoding yoxdur, Windows-da crash ede biler. | DUZELDILECEK |
| 4 | `language.py` | Butun `open()` cagirislari encoding olmadan — charmap xetasi. | DUZELDILDI |
| 5 | `main.py:78` | `extractCommands` encoding olmadan fayl oxuyur. | DUZELDILDI |

### 1.2 BRANDING PROBLEMLERI (86 kohne referans)

22 faylda `DTÖ`, `DTO`, `dto`, `userator`, `Userator`, `UseratorSUP`, `UseratorLang` referanslari qalir:

| Fayl | Say | Numuneler |
|------|-----|-----------|
| `modullar.py` | 18 | DTÖUserBot animasiya stringlerinde |
| `scrapers_bot.py` | 12 | dto devisken adlari |
| `rose.py` | 10 | dto devisken adlari |
| `store.py` | 10 | dto devisken adlari |
| `dil.py` | 7 | @UseratorLang, @UseratorSUP |
| `main.py` | 5 | dtotext devisken adi |
| `events.py` | 3 | dtotext devisken adi |
| `__init__.py` | 2 | DTÖUserBot referansi |
| `__plugin.py` | 2 | @UseratorSUP |
| `gadmin.py` | 1 | @UseratorSUP |
| `cevir.py` | 3 | DTO referanslari |
| `gdrive.py` | 3 | DTÖUserBot |
| `memes.py` | 1 | DTÖUserBot |
| `muah.py` | 1 | DTÖUserBot |
| `scrapers.py` | 1 | USERATOR |
| `www.py` | 1 | DTÖUserBot |
| `extra.py` | 1 | DTO referansi |
| `dorc.py` | 1 | DTO referansi |
| `anti_spambot.py` | 1 | DTO referansi |
| `esqolc.py` | 1 | DTO referansi |
| `db_backup.py` | 1 | USERATOR komment |
| `userator.py` | Butun fayl | Kohne ad, fayl adini deyismek lazim |

### 1.3 SYNTAX WARNINGS (Python 3.12+ ile xeta verecek)

| Fayl | Setir | Problem |
|------|-------|---------|
| `afk.py` | 129 | `"\{"` → `r"\{"` |
| `filter.py` | 192, 212 | `"\w"` → `r"\w"` |
| `modullar.py` | 55, 79, 456, 630 | `"\_"`, `"\ "` |
| `memes.py` | 983 | `"\_"` |
| `scrapers_bot.py` | 123 | `"\d"` → `r"\d"` |
| `snips.py` | 46, 107 | `"\w"` → `r"\w"` |
| `song.py` | 37 | `"\d"` → `r"\d"` |
| `store.py` | 109 | `"\w"` → `r"\w"` |
| `evaluators.py` | 33 | `is 'env'` → `== 'env'` |

### 1.4 ENCODING PROBLEMLERI

26+ faylda `open()` `encoding='utf-8'` olmadan istifade olunur.
Windows-da default CP1254 encoding UTF-8 simvollari oxuya bilmir.
Butun `open(..., 'r')` cagirislarina `encoding='utf-8'` elave edilmelidir.

### 1.5 EKSIK PAKETLER (Import xetalari)

Bu paketler qurasdirilibsa modullar isleyecek:

| Paket | Modullar |
|-------|----------|
| `Pillow` | photos, stickers, rgb, reverse, liste, deepfry, cevir, cnvrt |
| `emoji` | qrup, scrapers |
| `pySmartDL` | upload_download, gdrive, cnvrt |
| `youtube_dl` | song, ytdl |
| `pytz` | time, weather |
| `qrcode` | qrcode |
| `aiohttp` | github |
| `speedtest-cli` | www |
| `pydub` | shazam |
| `hachoir` | thum |
| `pylast` | lastfm |
| `lyricsgenius` | lyrics |
| `cowpy` | memes |
| `pybase64` | hash |
| `aria2p` | aria |
| `coffeehouse` | lydia (PyPI-da yoxdur - silinmeli) |

### 1.6 DIGER PROBLEMLER

| Problem | Izah |
|---------|------|
| `TG_BOT_TOKEN.session` | Root-da session fayli var, .gitignore-a elave edilmeli |
| `dto.db` | Kohne database fayli, silinmeli |
| `rebrand_to_apex.py` | Utility skript, siline biler |
| `fix_sql_tables.py` | Utility skript, siline biler |
| `ΣRROR.log` fayl adi | Unicode simvol OS problemleri yarada biler |

---

## 2. PYTHON VERSIYASI

**Tovsiye: Python 3.11**

| Versiya | Status |
|---------|--------|
| Python 3.9 | Kohne Dockerfile-da istifade olunurdu |
| Python 3.11 | **TOVSIYE** - Stabil, butun paketler deskekleyir |
| Python 3.12 | `distutils` deprecated, bezi paketler uygun deyil |
| Python 3.13+ | `distutils` silinib, Telethon uygunsuzluqlari |
| Python 3.14 | Event loop problemleri (duzeldildi amma risk var) |

**Dockerfile-da `python:3.11-slim` istifade olunur** - Dogru secimdir.

---

## 3. YARADICI (ADMIN) YOL XERITESI

### Addim 1: GitHub Repo Hazirligi

```
1. github.com-da hesab ac (varsa kec)
2. "New Repository" bas
   - Ad: apex-userbot (ve ya delta)
   - Public (pulsuz)
   - README elave etme (artiq var)
3. Lokal kompyuterden:
   cd C:\Users\wecde\OneDrive\Masaüstü\delta-master
   git init (artiq var)
   git remote add origin https://github.com/SENIN_USERNAME/apex-userbot.git
   git add .
   git commit -m "APEX Userbot v3.1"
   git branch -M main
   git push -u origin main
```

**DIQQET:** Push etmezden evvel:
- `config.env` faylinin `.gitignore`-da oldugunu yoxla
- `TG_BOT_TOKEN.session` faylini sil ve ya .gitignore-a elave et
- `dto.db`, `apex.db` gitignore-a elave et
- `rebrand_to_apex.py`, `fix_sql_tables.py` siline biler

### Addim 2: Setup Bot Yaratma

```
1. Telegram-da @BotFather-e /newbot yaz
   - Ad: APEX Setup Bot
   - Username: ApexSetupBot (ve ya baska)
   - TOKEN-i kopyala

2. HuggingFace-de hesab ac: huggingface.co/join
3. huggingface.co/new-space → Ad: apex-setup-bot → SDK: Docker
4. Space Settings > Secrets:
   - SETUP_BOT_TOKEN = BotFather token
   - GITHUB_REPO = https://github.com/SENIN_USERNAME/apex-userbot
5. setup_bot/ qovlugundaki fayllari Space-e yukle:
   - bot.py
   - requirements.txt
   - Dockerfile
6. Space build olacaq ve bot baslayacaq (2-3 deqiqe)
```

### Addim 3: Test

```
1. Telegram-da @ApexSetupBot-a /start yaz
2. /setup ile qurulumu test et
3. Oz hesabinla tam qurulum prosesini kecir
4. .alive emri ile botu yoxla
5. .dbbackup ile DB backup-i yoxla
```

### Addim 4: Yenileme Prosesi

```
Sen GitHub-da kod deyisirsen:
  git add .
  git commit -m "Yeni ozellik: ..."
  git push

Istifadeciler Telegram-da .update yazir:
  → HF Space restart olur
  → git pull son kodu cekir
  → DB backup-dan berpa olunur
  → Bot yeniden isleyir
```

### Addim 5: Qarsilasa Bileceyiniz Xetalar

| Xeta | Sebeb | Hell |
|------|-------|------|
| `git push rejected` | Remote-da ferqli fayl var | `git pull --rebase` sonra `git push` |
| HF Space build fail | Dockerfile xetasi ve ya paket problemi | HF Space logs-a bax |
| Bot Telegram-da cavab vermir | STRING_SESSION yanlis | Setup bot ile yeniden qur |
| `.update` islemir | HF_TOKEN ve ya HF_SPACE_ID yoxdur | Space secrets-e elave et |
| Modul yuklenmir | Paket qurasdirilibmayib | requirements.txt-e elave et |
| DB backup islemir | BOTLOG_CHATID yanlis ve ya qrup yoxdur | Qrup yarad, ID-ni duzelt |
| charmap encoding xetasi | open() encoding olmadan | encoding='utf-8' elave et |

---

## 4. LAYIHE STRUKTURU

```
apex-userbot/
├── .gitignore          # config.env, *.db, *.session ignore
├── Dockerfile          # HuggingFace ucun (Python 3.11)
├── Aptfile             # Sistem paketleri (neofetch, chromium)
├── LICENSE             # GPL-3.0
├── README.md           # Layihe haqqinda
├── app.py              # Flask server + Bot baslama
├── main.py             # Entry point (from userbot import main)
├── config.env.example  # Numune config
├── requirements.txt    # Python paketleri
│
├── setup_bot/          # Qurulum botu (ayri HF Space-de isleyir)
│   ├── bot.py
│   ├── Dockerfile
│   ├── requirements.txt
│   └── README.md
│
├── userbot/
│   ├── __init__.py     # Esas baslama, env yukleme, bot yaratma
│   ├── main.py         # Plugin yukleme, DB backup/restore
│   ├── events.py       # Event handler, xeta tutucu
│   ├── language.py     # Dil fayllari yukleme
│   ├── cmdhelp.py      # Emr yardim sistemi
│   ├── session_manager.py  # Avtomatik session yaratma
│   ├── google_imgs.py  # Google images axdarma
│   ├── language/       # Dil fayllari (.apexjson)
│   ├── fonts/          # Sriftler
│   └── modules/        # Butun pluginler/modullar
│       ├── __init__.py     # Modul siyahisi
│       ├── __helpme.py     # .help emri
│       ├── __plugin.py     # Plugin yukleme sistemi
│       ├── __up.py         # .apex emri
│       ├── admin.py        # Admin emrleri
│       ├── afk.py          # AFK sistemi
│       ├── db_backup.py    # DB backup/restore
│       ├── update.py       # .update emri (HF restart)
│       ├── ... (70+ modul)
│       └── sql_helper/     # Database modelleri
│           ├── __init__.py
│           └── *.py (17 SQL model)
└
```

---

## 5. PRIORITET SIRASI

1. **KRITIK** — events.py bug fix, distutils evezleme, branding temizleme
2. **YUKSEK** — SyntaxWarning-leri duzelt, encoding fix, .gitignore yenile
3. **ORTA** — Eksik paketleri requirements.txt-e elave et
4. **ASAGI** — Kohne utility skriptleri sil, README yenile
