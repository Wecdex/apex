# 🛠️ APEX Userbot — Yaradıcı Rehbəri

> Bu rehbər **layihənin sahibi** (sən) üçündür. GitHub-a yükləmək, Setup Bot-u deploy etmək və layihəni idarə etmək üçün addım-addım təlimat.

---

## 📐 Layihə Arxitekturası

```
Sən (Yaradıcı)
├── GitHub Repo (sahibziko/delta) ← kod burada saxlanır
├── HF Space #1: "Setup Bot" ← sən deploy edirsən, istifadəçilər bura yazır
│   └── setup_bot/bot.py (Telegram bot — istifadəçiləri qurur)
│
İstifadəçi
└── HF Space #2: "apex-userbot" ← Setup Bot avtomatik yaradır
    └── Dockerfile → app.py → main.py → userbot işləyir
```

**Axın:**
1. İstifadəçi Setup Bot-a yazır
2. Setup Bot API/Session/HF token toplayır
3. Setup Bot istifadəçinin HF Space-ini yaradır + secrets yerləşdirir
4. İstifadəçinin Space-i avtomatik build olur və userbot işləyir

---

## 📋 Addım 1 — GitHub Hesabı və Repo

### 1.1 GitHub hesabı
1. **[github.com](https://github.com)** saytında hesab açın (əgər yoxdursa)
2. Email-inizi təsdiqləyin

### 1.2 Yeni repo yaradın
1. **[github.com/new](https://github.com/new)** səhifəsinə keçin
2. Doldurun:
   - **Repository name:** `delta`
   - **Description:** `APEX Telegram Userbot`
   - **Visibility:** `Public` (HuggingFace pulsuz planda public olmalıdır)
   - **Add .gitignore:** seçməyin (artıq var)
   - **Add license:** seçməyin (artıq var)
3. **"Create repository"** basın

### 1.3 Faylları yükləyin

#### Variant A — Git ilə (tövsiyə olunur)
```bash
# 1. Git yükləyin (əgər yoxdursa): https://git-scm.com
# 2. Terminal/PowerShell açın, delta-master qovluğuna keçin:

cd "c:\Users\wecde\OneDrive\Masaüstü\delta-master"

# 3. Git başladın:
git init
git remote add origin https://github.com/sahibziko/delta.git

# 4. Bütün faylları əlavə edin:
git add .

# 5. İlk commit:
git commit -m "APEX Userbot v1.0"

# 6. GitHub-a göndərin:
git branch -M main
git push -u origin main
```

> ⚠️ GitHub sizin username/password-unuzu soruşacaq. Password yerinə **Personal Access Token** istifadə edin:
> GitHub → Settings → Developer settings → Personal access tokens → Generate new token

#### Variant B — Brauzerdən yükləmə (asan)
1. GitHub repo səhifəsinə keçin
2. **"uploading an existing file"** linkinə basın
3. Bütün faylları sürükləyin (`.git` qovluğu **XARİC**)
4. **"Commit changes"** basın

> ⚠️ Brauzerdən yükləmə zamanı böyük fayllar problem yarada bilər. Git tövsiyə olunur.

### 1.4 Yükləndiyini yoxlayın
`https://github.com/sahibziko/delta` açın, bu fayllar görünməlidir:
- `app.py`
- `main.py`
- `Dockerfile`
- `requirements.txt`
- `config.env.example`
- `userbot/` qovluğu
- `setup_bot/` qovluğu

---

## 📋 Addım 2 — Setup Bot-u HuggingFace-ə Deploy edin

Setup Bot istifadəçilərə userbot qurmağa kömək edən Telegram botudur. Sən bunu **bir dəfə** deploy edirsən.

### 2.1 HuggingFace hesabı
1. **[huggingface.co/join](https://huggingface.co/join)** hesab açın
2. Email-inizi təsdiqləyin

### 2.2 Yeni Space yaradın
1. **[huggingface.co/new-space](https://huggingface.co/new-space)** keçin
2. Doldurun:
   - **Space name:** `apex-setup-bot`
   - **License:** `MIT`
   - **SDK:** `Docker`
   - **Visibility:** `Public`
3. **"Create Space"** basın

### 2.3 Faylları yükləyin
Space-in **Files** tabına keçin və bu faylları yükləyin (`setup_bot/` qovluğundan):

| Fayl | Məzmun |
|------|--------|
| `Dockerfile` | `setup_bot/Dockerfile` |
| `bot.py` | `setup_bot/bot.py` |
| `requirements.txt` | `setup_bot/requirements.txt` |

> HF-də "Add file" → "Upload files" basın, 3 faylı seçin, "Commit" basın.

### 2.4 Secret əlavə edin (İSTƏYƏ BAĞLI)
Space → **Settings** → **Variables and secrets** bölməsinə keçin:

| Ad | Dəyər | Qeyd |
|----|-------|------|
| `SETUP_BOT_TOKEN` | `8627242727:AAF97myd1Yfw6PBK27u-Gu3s-3v43JfpCRs` | Bot tokeni artıq kod içindədir, amma secret olaraq da əlavə edə bilərsiniz |
| `GITHUB_REPO` | `https://github.com/sahibziko/delta` | Default olaraq artıq kodda var |

> Token artıq `bot.py` içindədir, amma gələcəkdə dəyişdirmək istəsəniz Secret vasitəsilə env var-dan oxuyacaq.

### 2.5 Gözləyin
- Space build olacaq (2-3 dəqiqə)
- Logs tabında `APEX Setup Bot isleyir...` mesajı görünməlidir
- Setup Bot artıq Telegram-da aktivdir!

### 2.6 Test edin
1. Telegram-da öz Setup Bot-unuza yazın
2. `/start` yazın
3. `/setup` yazın
4. Bütün addımları keçin — sonda sizin üçün userbot Space yaranmalıdır

---

## 📋 Addım 3 — Yeniləmə Prosesi

İstifadəçilərin botları avtomatik yenilənir. Siz GitHub-da dəyişiklik etdikdə:

### 3.1 Kod yeniləmə
```bash
cd "c:\Users\wecde\OneDrive\Masaüstü\delta-master"
git add .
git commit -m "v1.1 — bug fix / yeni modul"
git push
```

### 3.2 İstifadəçi tərəfi
İstifadəçilər Telegram-da `.update` yazanda:
1. Bot GitHub-dan `git pull` edəcək
2. Yeni kod yüklənəcək
3. Bot yenidən başlayacaq

> İstifadəçilərin Dockerfile-ında `git pull origin main` var — hər restart-da avtomatik yenilənir.

---

## 📋 Addım 4 — Problemlərin Həlli

### Setup Bot işləmir?
1. HF Space → Logs tabına baxın
2. `SETUP_BOT_TOKEN` düzgün olduğundan əmin olun
3. Space-i "Factory reboot" edin

### İstifadəçinin botu başlamır?
1. İstifadəçinin HF Space → Logs-a baxın
2. Ən çox rast gəlinən problemlər:
   - **API_KEY/API_HASH yanlışdır** → istifadəçi yenidən `/setup` etməlidir
   - **STRING_SESSION vaxtı keçib** → yeni session yaradılmalıdır
   - **Port 7860 problemi** → app.py-da Flask server düzgün işləmir

### requirements.txt xətası?
Bəzi paketlər müəyyən OS-da quraşdırılmır. `Dockerfile`-da `|| true` var — bu paketlər skip ediləcək, əsas paketlər işləyəcək.

### Yeni modul əlavə etmək
1. `userbot/modules/` qovluğuna `.py` faylı əlavə edin
2. `git push` edin
3. İstifadəçilər `.update` yazanda yenilənəcək

---

## 📋 Addım 5 — Gündəlik İdarəetmə

### Setup Bot-un Telegram username-ini dəyişdirmək
1. Telegram-da **@BotFather**-a yazın
2. `/mybots` → botunuzu seçin → **Edit Bot** → **Edit Username**

### Yeni bot token almaq (lazım olarsa)
1. @BotFather → `/mybots` → botunuzu seçin → **API Token** → **Revoke**
2. Yeni tokeni `setup_bot/bot.py`-da dəyişdirin
3. HF Space-də Secret-i yeniləyin
4. Space-i reboot edin

### GitHub repo-nu private etmək
> ⚠️ HF pulsuz planda private repo-dan pull edə bilmir!
> Əgər private etmək istəyirsinizsə, HF Space-in Dockerfile-ını dəyişdirməlisiniz — git clone əvəzinə faylları birbaşa COPY etməlisiniz.

---

## 🗂️ Fayl Strukturu

```
delta-master/
├── app.py                    ← HF Space üçün Flask launcher
├── main.py                   ← Bot-u başladan əsas fayl
├── Dockerfile                ← İstifadəçinin HF Space-i üçün
├── requirements.txt          ← Python paketləri
├── config.env.example        ← Lokal test üçün nümunə konfiqurasiya
├── .gitignore                ← Session/DB/env fayllarını ignore edir
│
├── userbot/
│   ├── __init__.py           ← Əsas bot inisializasiyası
│   ├── events.py             ← Xəta idarəsi + event handler
│   ├── main.py               ← Modulları yükləyən launcher
│   ├── language.py           ← Dil sistemi
│   ├── cmdhelp.py            ← Əmr yardım sistemi
│   ├── modules/              ← 40+ modul (admin, afk, song, meme...)
│   │   ├── db_backup.py      ← Avtomatik DB backup/restore
│   │   ├── update.py         ← .update əmri
│   │   ├── store.py          ← Plugin mağazası
│   │   └── ...
│   ├── language/             ← Dil faylları (AZ, TR, EN, RU)
│   └── modules/sql_helper/   ← SQLAlchemy ORM modelləri
│
├── setup_bot/
│   ├── bot.py                ← Setup Bot əsas kodu
│   ├── Dockerfile            ← Setup Bot HF Space üçün
│   └── requirements.txt      ← Setup Bot paketləri
│
├── ISTIFADECI_REHBERI.md     ← İstifadəçi üçün addım-addım rehbər
└── YARADICI_REHBERI.md       ← Bu fayl (sən üçün)
```

---

## ✅ Çek-list

- [ ] GitHub hesabı açıldı
- [ ] GitHub repo yaradıldı (`sahibziko/delta`)
- [ ] Bütün fayllar GitHub-a yükləndi
- [ ] HuggingFace hesabı açıldı
- [ ] Setup Bot üçün HF Space yaradıldı (`apex-setup-bot`)
- [ ] Setup Bot faylları yükləndi (3 fayl)
- [ ] Setup Bot işləyir (Logs-da `isleyir` mesajı)
- [ ] Test qurulum keçirildi
- [ ] İstifadəçilərə Setup Bot linki paylaşıldı

---

## 🆘 Dəstək lazımdırsa
Telegram: **@apexsup**
