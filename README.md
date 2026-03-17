---
title: APEX Userbot
emoji: ⚡
colorFrom: purple
colorTo: red
sdk: docker
pinned: false
duplicated_from:
---

# 𝙰 𝙿 Σ 𝚇 ✨ — Telegram Userbot

## 🚀 Quraşdırma (Çox Asandır!)

### 1-ci Addım: String Session alın
> Əvvəlcə [my.telegram.org](https://my.telegram.org) saytından **API ID** və **API Hash** alın.
> Sonra String Session almaq üçün bu botu işlədin: **@StringFatherBot**

### 2-ci Addım: Bu Space-i kopyalayın
Yuxarıdakı **"Duplicate this Space"** düyməsinə basın və açılan pəncərədə bu dəyərləri doldurun:

| Dəyişkən | Nədir? |
|----------|--------|
| `API_KEY` | my.telegram.org-dan aldığınız API ID (rəqəm) |
| `API_HASH` | my.telegram.org-dan aldığınız API Hash |
| `STRING_SESSION` | @StringFatherBot-dan aldığınız kod |
| `BOTLOG_CHATID` | Log qrupunuzun ID-si (qrupda @userinfobot ilə öyrənin) |

### 3-cü Addım: Gözləyin
Space qurulacaq (2-3 dəqiqə). Sonra hər hansı söhbətə `.alive` yazın — bot cavab verəcək!

### 4-cü Addım: UptimeRobot (botun sönməməsi üçün)
1. [uptimerobot.com](https://uptimerobot.com) saytında pulsuz hesab açın
2. **Add New Monitor** basın
3. Type: `HTTP(s)`, URL: `sizin Space URL + /health`, Interval: `5 min`
4. Hazırdır! Bot heç vaxt sönməyəcək ⚡

---

## 💻 Lokal Test (Öz Kompyuterinizdə)

HuggingFace-ə deploy etməzdən əvvəl botu öz kompyuterinizdə test edə bilərsiniz:

### Windows üçün:

1. **Konfiqurasiya faylı yaradın:**
   ```bash
   copy config.env.example config.env
   ```
   Sonra `config.env` faylını açıb dəyərləri doldurun (API_KEY, STRING_SESSION və s.)

2. **Botu işə salın:**
   - **PowerShell:** `.\run.ps1`
   - **CMD:** `run.bat`

3. **Test edin:**
   - Bot `http://localhost:7860` ünvanında işləyəcək
   - Telegram-da `.alive` əmrini yoxlayın

**Qeyd:** Lokal test HuggingFace deploy-a mane olmur. Eyni konfiqurasiya hər iki yerdə işləyir!

---

**Dəstək:** [@apexsup](https://t.me/apexsup) | **Kanal:** [@apexuserbot](https://t.me/apexuserbot)
