# APEX Userbot - Setup Bot

Telegram vasitesile avtomatik userbot qurulum botu.

## Bu ne edir?

Istifadeciler bu bota `/setup` yazaraq 5 deqiqe erzinde pulsuz userbot qura bilir:
1. STRING_SESSION yaradir
2. BOTLOG qrupu yaradir
3. HuggingFace Space acir
4. Butun secret-leri avtomatik teyin edir
5. Userbot isleyir!

## Deploy (Admin ucun)

### 1. Telegram Bot yarad
- @BotFather-e `/newbot` yaz
- Bot adini ver (mes: APEX Setup Bot)
- Token-i kopyala

### 2. HuggingFace Space yarat
- https://huggingface.co/new-space adresine get
- Ad: `apex-setup-bot`
- SDK: **Docker**
- Visibility: **Public** (free tier)

### 3. Secret-leri teyin et
Space Settings > Variables and Secrets:
- `SETUP_BOT_TOKEN` = BotFather-den aldigin token
- `GITHUB_REPO` = https://github.com/sahibziko/delta (istege bagli)

### 4. Fayllari yukle
`setup_bot/` qovlugundaki butun fayllari Space-e yukle:
- `bot.py`
- `requirements.txt`
- `Dockerfile`

### 5. Hazir!
Bot avtomatik baslayacaq. Istifadeciler bota `/start` yazaraq quruluma baslaya biler.

## Istifadeci Tecrubesi

```
Istifadeci: /start
Bot: Xos geldiniz! /setup yazin.

Istifadeci: /setup
Bot: API ID gonderin:
Istifadeci: 12345678
Bot: API Hash gonderin:
Istifadeci: abcdef...
Bot: Telefon nomresi gonderin:
Istifadeci: +994501234567
Bot: Tesdiq kodu gonderin:
Istifadeci: 1 2 3 4 5
Bot: HuggingFace token gonderin:
Istifadeci: hf_xxxxx
Bot: Userbot quruldu! 3-5 deqiqe gozleyin.
```

## Texniki Detallar

- **python-telegram-bot** v20+ (async) - Setup bot UI
- **telethon** - STRING_SESSION yaratma
- **huggingface_hub** - Space yaratma ve secret teyin etme
- Her istifadeci ucun ayri HuggingFace Space yaradilir
- Space Dockerfile vasitesile GitHub-dan kodu cekir
- `.update` emri Space-i restart edir, `git pull` son kodu cekir
