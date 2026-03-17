# 🚀 Tam Quraşdırma Təlimatı

Bu təlimat **həm lokal test**, **həm də HuggingFace deploy** üçün addım-addım bələdçidir.

---

## 📋 Ön Hazırlıq

### 1. Telegram API Məlumatları

**a) API ID və API Hash alın:**
1. [my.telegram.org](https://my.telegram.org) saytına daxil olun
2. **API Development Tools** bölməsinə keçin
3. Yeni tətbiq yaradın (istənilən ad)
4. **API ID** (rəqəm) və **API Hash** (uzun kod) kopyalayın

**b) String Session alın:**
1. Telegram-da [@StringFatherBot](https://t.me/StringFatherBot) botunu açın
2. `/start` yazın
3. **Pyrogram** və ya **Telethon** seçin (Telethon tövsiyə olunur)
4. API ID və API Hash daxil edin
5. Telefon nömrənizi daxil edin (+994... formatında)
6. Telegram-dan gələn kodu daxil edin
7. Alınan **String Session**-u kopyalayın (çox uzun kod)

**c) Log Qrupu yaradın:**
1. Telegram-da özünüzə xüsusi qrup yaradın
2. [@userinfobot](https://t.me/userinfobot) botunu qrupa əlavə edin
3. Qrupun **ID**-sini kopyalayın (məs: `-100123456789`)

---

## 💻 Variant 1: Lokal Test (Windows)

### Addım 1: Konfiqurasiya

```cmd
copy config.env.example config.env
```

`config.env` faylını açıb bu dəyərləri doldurun:

```env
API_KEY=12345678
API_HASH=abcdef1234567890abcdef1234567890
STRING_SESSION=1BVtsOLwBu...
BOTLOG_CHATID=-100123456789
BOTLOG=True
```

### Addım 2: İşə Salma

**PowerShell:**
```powershell
.\run.ps1
```

**CMD:**
```cmd
run.bat
```

Skript avtomatik:
- Python virtual environment yaradacaq
- Bütün paketləri quraşdıracaq (2-3 dəqiqə)
- Botu işə salacaq

### Addım 3: Yoxlama

1. Brauzer: `http://localhost:7860` (bot statusu görməlisiniz)
2. Telegram: İstənilən söhbətə `.alive` yazın

**Dayandırmaq üçün:** `Ctrl+C`

---

## ☁️ Variant 2: HuggingFace Deploy (24/7 İşləyir)

### Addım 1: HuggingFace Hesabı

1. [huggingface.co](https://huggingface.co) saytında hesab yaradın (pulsuz)
2. Giriş edin

### Addım 2: Space Yaradın

1. **Spaces** → **Create new Space**
2. **Space name:** `apex-userbot` (və ya istədiyiniz ad)
3. **SDK:** **Docker** seçin ⚠️
4. **Public** və ya **Private** seçin
5. **Create Space**

### Addım 3: Kodu Yükləyin

**Variant A: Git ilə (tövsiyə olunur):**

```bash
git clone https://huggingface.co/spaces/YOUR_USERNAME/apex-userbot
cd apex-userbot
# Bu layihənin fayllarını kopyalayın (config.env istisna olmaqla!)
git add .
git commit -m "Initial commit"
git push
```

**Variant B: Web interfeys ilə:**

1. Space səhifəsində **Files** tab-ına keçin
2. Bütün faylları bir-bir yükləyin (`.gitignore`-dakı fayllar istisna)

### Addım 4: Environment Variables

1. Space səhifəsində **Settings** → **Variables and secrets**
2. Bu dəyərləri əlavə edin:

| Name | Value | Type |
|------|-------|------|
| `API_KEY` | 12345678 | Secret |
| `API_HASH` | abcdef... | Secret |
| `STRING_SESSION` | 1BVtsOLw... | Secret |
| `BOTLOG_CHATID` | -100123456789 | Secret |
| `BOTLOG` | True | Public |

⚠️ **Hamısını Secret olaraq seçin!**

### Addım 5: Build və İşə Salma

1. **Settings** → **Factory reboot** (və ya sadəcə gözləyin)
2. Build prosesi başlayacaq (3-5 dəqiqə)
3. Status **Running** olduqda hazırdır

### Addım 6: Test

1. Space URL-ni açın (məs: `https://YOUR_USERNAME-apex-userbot.hf.space`)
2. "✅ Aktiv" görməlisiniz
3. Telegram-da `.alive` yazın

---

## 🔄 UptimeRobot (24/7 Aktiv Qalması Üçün)

HuggingFace Spaces 48 saat aktivlik olmayanda yuxu rejiminə keçir. Bunu qarşısını almaq üçün:

### Addım 1: UptimeRobot Hesabı

1. [uptimerobot.com](https://uptimerobot.com) saytında pulsuz hesab yaradın
2. Giriş edin

### Addım 2: Monitor Yaradın

1. **Add New Monitor**
2. **Monitor Type:** `HTTP(s)`
3. **Friendly Name:** `APEX Userbot`
4. **URL:** `https://YOUR_USERNAME-apex-userbot.hf.space/health`
5. **Monitoring Interval:** `5 minutes`
6. **Create Monitor**

Artıq bot heç vaxt sönməyəcək! ⚡

---

## 📝 Əsas Əmrlər

| Əmr | Təsvir |
|-----|--------|
| `.alive` | Bot statusu |
| `.help` | Bütün əmrlər |
| `.ping` | Ping yoxla |
| `.sysd` | Sistem məlumatları |
| `.ban` | İstifadəçini banla |
| `.kick` | İstifadəçini qrupdan çıxart |
| `.mute` | İstifadəçini sustur |
| `.purge` | Mesajları sil |
| `.afk` | AFK rejimi |

Tam siyahı üçün: `.help`

---

## ❓ Tez-tez Verilən Suallar

### ❓ Lokal test HuggingFace-ə mane olurmu?
**Cavab:** Xeyr! Eyni konfiqurasiya hər iki yerdə işləyir.

### ❓ config.env faylını GitHub-a push edə bilərəmmi?
**Cavab:** XEYİR! ⚠️ Bu faylda gizli məlumatlar var. `.gitignore` onu qoruyur.

### ❓ HuggingFace-də config.env lazımdırmı?
**Cavab:** Xeyr. HF-də Environment Variables istifadə olunur.

### ❓ Bot niyə cavab vermir?
**Cavab:** 
- STRING_SESSION düzgündürmü yoxlayın
- BOTLOG_CHATID mənfi rəqəmdirmi yoxlayın
- Telegram-da hesabınız aktiv olmalıdır

### ❓ Port 7860 dəyişə bilərəmmi?
**Cavab:** Lokalda bəli (`app.py`-də), amma HF-də xeyr (7860 məcburidir).

### ❓ Neçə hesabda işlədə bilərəm?
**Cavab:** Hər String Session bir hesaba aiddir. Hər hesab üçün ayrı Space lazımdır.

---

## 🛠️ Problemlər və Həllər

### ❌ "PhoneNumberInvalidError"
**Səbəb:** String Session düzgün deyil  
**Həll:** @StringFatherBot-dan yenidən alın

### ❌ "BOTLOG_CHATID xətası"
**Səbəb:** Qrup ID düzgün deyil və ya icazə yoxdur  
**Həll:** 
- ID mənfi rəqəm olmalıdır (`-100...`)
- Qrupda admin olmalısınız

### ❌ "FloodWaitError"
**Səbəb:** Telegram spam qoruması  
**Həll:** 10-15 dəqiqə gözləyin

### ❌ Build uğursuz oldu (HF)
**Səbəb:** Environment variables düzgün deyil  
**Həll:** Settings-də yenidən yoxlayın

---

## 📞 Dəstək

- **Qrup:** [@apexsup](https://t.me/apexsup)
- **Kanal:** [@apexuserbot](https://t.me/apexuserbot)

---

**Uğurlar! 🚀**
