# APEX Userbot - Istifadeci Qurulum Rehberi

## Nedir?
APEX pulsuz Telegram userbotudur. Hesabinizi bota cevirir ve 70+ emr ile isleye bilirsiniz.

## Ne Lazimdir?
1. Telegram hesabi (telefon nomresi ile)
2. HuggingFace hesabi (pulsuz) - huggingface.co

## Qurulum (5 deqiqe)

### Addim 1: Telegram API melumatlari
1. https://my.telegram.org/auth saytina daxil olun
2. Telefon nomrenizi yazin, gelen kodu daxil edin
3. "API development tools" bolmesine kecin
4. Eger form cixarsa doldurun:
   - App title: APEX
   - Short name: apex
   - Platform: Other
5. `api_id` (reqem) ve `api_hash` (32 simvol) gorsenecek
6. Bunlari bir yere kopyalayin

### Addim 2: HuggingFace hesabi
1. https://huggingface.co/join saytina daxil olun
2. Hesab yaradiniz (email, sifre)
3. https://huggingface.co/settings/tokens adresine kecin
4. "Create new token" basin
   - Ad: apex
   - Type: Write
5. Token-i kopyalayin (hf_... ile baslayir)

### Addim 3: Setup Bot ile qurulum
1. Telegram-da @ApexSetupBot-a yazin
2. /start basin
3. /setup basin
4. Bot sizden sorusacaq:
   - API ID → reqemi gonderin
   - API Hash → 32 simvollu metni gonderin
   - Telefon nomresi → +994501234567 formatinda
   - Tesdiq kodu → Telegram-dan gelen kodu bosluqlarla yazin: 1 2 3 4 5
   - 2FA sifresi → (varsa) sifrenizi yazin
   - HuggingFace token → hf_... token-i gonderin
5. Bot avtomatik:
   - STRING_SESSION yaradacaq
   - BOTLOG qrupu yaradacaq
   - HuggingFace Space acacaq
   - Butun ayarlari edecek

### Addim 4: Gozleyin
- Bot 3-5 deqiqe erzinde aktivlesecek
- Ilk defe Docker build oldugu ucun bir az uzun cekir

### Addim 5: Test edin
- Telegram-da her hansi sohbete `.alive` yazin
- Bot cavab verirse - isleyir!

## Esas Emrler

| Emr | Izah |
|-----|------|
| `.alive` | Bot aktiv oldugunu yoxla |
| `.help` | Butun emrler |
| `.update` | Botu yenile (son versiyanı yukle) |
| `.dbbackup` | Database backup al |
| `.dbrestore` | Database berpa et |
| `.afk` | AFK rejimini aktiv et |
| `.ping` | Bot suretini yoxla |

## Tez-tez Verilen Suallar

**S: Bot nece pulsuz isleyir?**
C: HuggingFace pulsuz server verir. Bot orada isleyir.

**S: Telefonum sondurulse bot isleyir?**
C: Beli! Bot HuggingFace serverinde isleyir, telefonunuzdan asili deyil.

**S: Bot nece yenilenir?**
C: Telegram-da `.update` yazin. Bot avtomatik yenilenecek.

**S: Melumatlarim (database) itir?**
C: Xeyr. Bot her 6 saatda avtomatik backup alir. Restart zamani berpa olunur.

**S: Bir nece hesabda istifade ede bilerem?**
C: Her hesab ucun ayri qurulum lazimdir. Setup bot-a yeniden /setup yazin.

**S: Botu nece sondururem?**
C: HuggingFace-de Space-i pause edin ve ya silin.

**S: 2FA kodu nedir?**
C: Telegram hesabinizda iki faktorlu tesdiq aktivdirsə, setup bot sizden 2FA sifresini sorusacaq. Yokdursa bu addim atlanir.

## Problem Hell

| Problem | Hell |
|---------|------|
| Bot `.alive`-a cavab vermir | 5 deqiqe gozleyin. HF Space hala build ola biler. |
| "API ID yanlis" xetasi | my.telegram.org-dan yeniden yoxlayin |
| "Kod yanlis" xetasi | Kodu bosluqlarla yazin: 1 2 3 4 5 |
| "HF token yanlis" | Token hf_ ile baslamalidir. Write icazesi olmalidir. |
| Bot bir muddet sonra dayanir | HF free tier 72 saat sonra sleep edir. Space-i yeniden basladiniz. |
