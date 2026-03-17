# 📱 APEX Userbot — İstifadəçi Qurulum Rehbəri

> Bu rehbər sizə **5 dəqiqə** ərzində pulsuz Telegram userbot qurmağa kömək edəcək.

---

## 🔧 Lazım olanlar

| # | Nə lazımdır | Haradan alınır |
|---|-------------|----------------|
| 1 | Telegram hesabı | Artıq var |
| 2 | Telegram API ID + Hash | [my.telegram.org](https://my.telegram.org) |
| 3 | HuggingFace hesabı (pulsuz) | [huggingface.co](https://huggingface.co/join) |

---

## 📋 Addım-addım Qurulum

### Addım 1 — Telegram API məlumatlarını alın

1. Brauzerinizdə **[my.telegram.org](https://my.telegram.org/auth)** saytına daxil olun
2. Telefon nömrənizi daxil edin (beynəlxalq format: `+994XXXXXXXXX`)
3. Telegram-dan gələn kodu yazın
4. **"API development tools"** bölməsinə keçin
5. Əgər ilk dəfədirsə, form doldurun:
   - **App title:** `APEX` (və ya istədiyiniz ad)
   - **Short name:** `apex`
   - **Platform:** `Other`
6. **API ID** (rəqəm) və **API Hash** (32 simvolluq mətn) qeyd edin

> ⚠️ Bu məlumatları heç kimə verməyin!

---

### Addım 2 — HuggingFace hesabı açın

1. **[huggingface.co/join](https://huggingface.co/join)** saytında pulsuz hesab açın
2. Email-inizi təsdiqləyin
3. **[huggingface.co/settings/tokens](https://huggingface.co/settings/tokens)** səhifəsinə keçin
4. **"Create new token"** basın:
   - **Ad:** `apex`
   - **Type:** `Write` (yazmaq icazəsi)
5. Yaranan token-i kopyalayın (`hf_...` ilə başlayır)

> ⚠️ Token-i saxlayın, bir daha göstərilməyəcək!

---

### Addım 3 — Setup Bot ilə qurulum

1. Telegram-da **@ApexSetupBot** botuna yazın (və ya yaradıcının sizə verdiyi bot linkinə keçin)
2. `/start` yazın — bot sizə təlimatları göstərəcək
3. `/setup` yazın — qurulum başlayacaq
4. Bot sizdən **addım-addım** soruşacaq:
   - **API ID** → Addım 1-dən aldığınız rəqəm
   - **API Hash** → Addım 1-dən aldığınız 32 simvolluq mətn
   - **Telefon nömrəsi** → `+994XXXXXXXXX` formatında
   - **Təsdiq kodu** → Telegram-dan gələn 5 rəqəmli kod (boşluqlarla: `1 2 3 4 5`)
   - **2FA şifrə** (əgər varsa) → İki faktorlu təsdiq şifrəniz
   - **HuggingFace Token** → Addım 2-dən aldığınız `hf_...` token
5. Bot avtomatik olaraq:
   - ✅ String Session yaradacaq
   - ✅ BOTLOG qrupu açacaq
   - ✅ HuggingFace Space yaradacaq
   - ✅ Botu quracaq və işə salacaq

---

### Addım 4 — Gözləyin və test edin

1. Bot sizə Space linkini verəcək
2. **3-5 dəqiqə** gözləyin (ilk dəfə Docker build olur)
3. Telegram-da **istənilən söhbətə** `.alive` yazın
4. Cavab gəlsə — **bot işləyir!** 🎉

---

## 🎮 Əsas Əmrlər

| Əmr | Nə edir |
|-----|---------|
| `.alive` | Botun aktiv olub-olmadığını yoxlayır |
| `.help` | Bütün əmrlərin siyahısı |
| `.ping` | Cavab müddətini ölçür |
| `.update` | Botu yeniləyir |
| `.dbbackup` | Verilənlər bazasını backup edir |
| `.dbrestore` | Backup-dan bərpa edir |
| `.afk <səbəb>` | AFK rejimini aktivləşdirir |
| `.store <ad>` | Plugin mağazasından plugin yükləyir |
| `.carbon <kod>` | Kod-dan gözəl şəkil yaradır |
| `.song <ad>` | Musiqi axtarır və yükləyir |
| `.tr <dil> <mətn>` | Tərcümə edir |
| `.tts <mətn>` | Mətni səsə çevirir |
| `.shutdown` | Botu söndürür |
| `.restart` | Botu yenidən başladır |

---

## ❓ Tez-tez Verilən Suallar (FAQ)

### Bot `.alive`-a cavab vermir?
1. HuggingFace Space-inizin linkini açın
2. Əgər "Building" yazırsa — hələ hazır deyil, gözləyin
3. Əgər "Running" yazırsa amma cavab yoxdur — Space-i "Factory reboot" edin
4. Əgər "Error" yazırsa — Settings → Logs bölməsinə baxın

### Bot dayanıb / yatıb?
HuggingFace pulsuz planlarda Space 48 saat fəaliyyətsizlikdən sonra yata bilər. Space-in linkini açsanız yenidən oyanacaq.

### String Session nədir?
Telegram hesabınıza bot kimi qoşulmaq üçün istifadə olunan bir açardır. Setup Bot bunu avtomatik yaradır.

### Məlumatlarım təhlükəsizdir?
- API ID/Hash — yalnız sizin HF Space-inizin secrets bölməsində saxlanır
- String Session — yalnız HF secrets-də saxlanır, heç kim görə bilməz
- Setup Bot heç bir məlumatınızı saxlamır

### Botu necə silim?
1. [huggingface.co/spaces](https://huggingface.co) → Space-inizi tapın
2. Settings → "Delete this Space" basın

---

## 🆘 Dəstək

Problem yaşayırsınız? **@apexsup** qrupuna yazın.
