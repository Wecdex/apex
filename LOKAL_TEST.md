# 💻 Lokal Test Təlimatı

Bu təlimat botu **öz kompyuterinizdə** test etmək üçündür. HuggingFace-ə deploy etməzdən əvvəl lokal test etmək tövsiyə olunur.

## ✅ Tələblər

- **Python 3.9+** ([yükləyin](https://www.python.org/downloads/))
- **Git** (istəyə bağlı)
- **Telegram hesabı** və API məlumatları

---

## 🚀 Addım-addım Quraşdırma

### 1️⃣ Konfiqurasiya Faylı Yaradın

```bash
# PowerShell və ya CMD-də:
copy config.env.example config.env
```

### 2️⃣ config.env Faylını Doldurun

`config.env` faylını mətn redaktoru ilə açın və bu dəyərləri doldurun:

```env
# MÜTLƏQDİR:
API_KEY=12345678                          # my.telegram.org-dan
API_HASH=abcdef1234567890...              # my.telegram.org-dan
STRING_SESSION=1BVtsOLwBu...              # @StringFatherBot-dan
BOTLOG_CHATID=-100123456789               # Log qrupunun ID-si
BOTLOG=True

# İSTƏYƏ BAĞLI:
LANGUAGE=DEFAULT
ALIVE_NAME=Mənim Adım
```

**Necə alınır:**
- **API_KEY & API_HASH:** [my.telegram.org](https://my.telegram.org) → API Development Tools
- **STRING_SESSION:** Telegram-da [@StringFatherBot](https://t.me/StringFatherBot) botu ilə
- **BOTLOG_CHATID:** Özünüzə qrup yaradın, [@userinfobot](https://t.me/userinfobot) əlavə edin, qrup ID-sini kopyalayın

### 3️⃣ Botu İşə Salın

**PowerShell üçün:**
```powershell
.\run.ps1
```

**CMD üçün:**
```cmd
run.bat
```

Skript avtomatik:
- Virtual environment yaradacaq
- Bütün asılılıqları quraşdıracaq
- Botu başladacaq

### 4️⃣ Test Edin

Bot işə düşdükdən sonra:

1. **Web interfeys:** Brauzerə `http://localhost:7860` yazın
2. **Health check:** `http://localhost:7860/health` (OK görməlisiniz)
3. **Telegram test:** İstənilən söhbətə `.alive` yazın

---

## 🔧 Əmrlər

| Əmr | Təsvir |
|-----|--------|
| `.alive` | Bot işləyirmi yoxla |
| `.help` | Bütün əmrləri gör |
| `.sysd` | Sistem məlumatları |
| `.ping` | Ping yoxla |

---

## ❓ Problemlər və Həllər

### ❌ "config.env tapılmadı"
**Həll:** `config.env.example` faylını `config.env` adı ilə kopyalayın

### ❌ "Python tapılmadı"
**Həll:** Python 3.9+ quraşdırın və PATH-a əlavə edin

### ❌ "PhoneNumberInvalidError"
**Həll:** STRING_SESSION düzgün deyil. Yenidən @StringFatherBot-dan alın

### ❌ "BOTLOG_CHATID xətası"
**Həll:** 
- Qrup ID-si mənfi rəqəm olmalıdır (məs: `-100123456789`)
- Qrupda mesaj göndərmə icazəniz olmalıdır

### ❌ Port 7860 məşğuldur
**Həll:** `app.py`-də portu dəyişdirin və ya məşğul olan prosesi bağlayın

---

## 🌐 HuggingFace-ə Deploy

Lokal test uğurlu olduqdan sonra HuggingFace-ə deploy edə bilərsiniz:

1. HuggingFace Space yaradın (Docker SDK)
2. **Settings → Variables and secrets** bölməsinə gedin
3. `config.env`-dəki eyni dəyərləri Environment Variables kimi əlavə edin:
   - `API_KEY`
   - `API_HASH`
   - `STRING_SESSION`
   - `BOTLOG_CHATID`
   - `BOTLOG`
4. Space avtomatik build olacaq və işə düşəcək

**VACIB:** `config.env` faylını GitHub-a push etməyin! (`.gitignore`-da var)

---

## 📝 Qeydlər

- Lokal test zamanı SQLite DB istifadə olunur (`apx.db`)
- HuggingFace-də də eyni DB sistemi işləyir
- Lokal test HuggingFace deploy-a heç bir mane olmur
- Hər iki mühitdə eyni konfiqurasiya işləyir

---

**Suallarınız varsa:** [@apexsup](https://t.me/apexsup)
