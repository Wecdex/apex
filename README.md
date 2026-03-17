# 𝙰 𝙿 Σ 𝚇 — Telegram Userbot

**Pulsuz, güclü və asan qurulum ilə Telegram Userbot.**

Telegram hesabınızı genişləndirin: admin idarəetmə, musiqi yükləmə, tərcümə, stiker oğurluğu, AFK rejimi və 40+ modul.

---

## 📱 Qurulum (5 dəqiqə)

### Nə lazımdır?

| # | Nə | Haradan | Vaxt |
|---|----|---------|------|
| 1 | Telegram hesabı | Artıq var | — |
| 2 | Telegram API ID + Hash | [my.telegram.org](https://my.telegram.org/auth) | 2 dəq |
| 3 | HuggingFace hesabı (pulsuz) | [huggingface.co](https://huggingface.co/join) | 1 dəq |

---

### Addım 1 — Telegram API məlumatlarını alın

1. **[my.telegram.org/auth](https://my.telegram.org/auth)** saytını brauzerdə açın
2. Telefon nömrənizi yazın: `+994XXXXXXXXX` (beynəlxalq format)
3. Telegram-dan gələn kodu daxil edin
4. **"API development tools"** bölməsinə keçin
5. Əgər ilk dəfədirsə form doldurun:
   - **App title:** `myapp` (istədiyiniz ad)
   - **Short name:** `myapp`
   - **Platform:** `Other`
6. Sizə göstərilən **API ID** (rəqəm) və **API Hash** (32 simvolluq mətn) qeyd edin

> ⚠️ **Bu məlumatları heç kimə verməyin!** Bunlar Telegram hesabınıza girişi təmin edən açarlardır.

**Xəta ola bilər:**
- *"Too many tries"* → 10-15 dəqiqə gözləyin, yenidən cəhd edin
- *Səhifə açılmır* → VPN yandırın, bəzi ölkələrdə bloklanıb
- *Kod gəlmir* → Telegram-ın Saved Messages-ə baxın, bəzən ora gəlir

---

### Addım 2 — HuggingFace hesabı açın

1. **[huggingface.co/join](https://huggingface.co/join)** saytında hesab açın
2. Email-inizi təsdiqləyin (spam qovluğuna da baxın)
3. **[huggingface.co/settings/tokens](https://huggingface.co/settings/tokens)** səhifəsinə keçin
4. **"Create new token"** basın:
   - **Ad:** `apex` (istədiyiniz)
   - **Type:** Mütləq **Write** seçin!
5. Yaranan tokeni kopyalayın (`hf_...` ilə başlayır)

> ⚠️ Token **bir dəfə** göstərilir! Kopyalayıb saxlayın.

**Xəta ola bilər:**
- *Token yaratma düyməsi yoxdur* → Email-inizi təsdiqləməlisiniz
- *"Read" seçdim* → Silyin, yenidən **Write** olaraq yaradın. Read işləməyəcək.

---

### Addım 3 — Setup Bot ilə qurulum

1. Telegram-da **Setup Bot**-a yazın (link yaradıcı tərəfindən veriləcək)
2. `/start` yazın
3. `/setup` yazın — qurulum başlayır
4. Bot addım-addım soruşacaq:

| Addım | Nə soruşur | Nə yazmalısınız |
|-------|-----------|-----------------|
| 1 | API ID | `12345678` (rəqəm) |
| 2 | API Hash | `abcdef1234567890abcdef1234567890` (32 simvol) |
| 3 | Telefon | `+994501234567` |
| 4 | Kod | `1 2 3 4 5` (boşluqlarla ayırın!) |
| 4.5 | 2FA şifrə (varsa) | İki faktorlu təsdiq şifrəniz |
| 5 | HuggingFace Token | `hf_abc...` |

5. Bot avtomatik olaraq:
   - ✅ String Session yaradacaq
   - ✅ BOTLOG qrupu açacaq
   - ✅ HuggingFace Space yaradacaq
   - ✅ Bütün parametrləri quracaq
   - ✅ Botu işə salacaq

**Xətalar və həlləri:**

| Xəta | Səbəb | Həll |
|------|-------|------|
| *"API ID rəqəm olmalıdır"* | Hərf yazmısınız | Yalnız rəqəm göndərin |
| *"API Hash 32 simvol olmalıdır"* | Natamam kopyalama | my.telegram.org-dan tam kopyalayın |
| *"Telefon nömrəsi yanlışdır"* | Yanlış format | `+994XXXXXXXXX` yazın, ölkə kodu ilə |
| *"Kod yanlışdır"* | Səhv kod və ya vaxt keçib | Kodu tez daxil edin, 5 dəq var |
| *"2FA şifrə yanlışdır"* | Səhv şifrə | Telegram Settings → Two-Step Verification şifrəniz |
| *"Telegram flood limit"* | Çox cəhd etmisiniz | Göstərilən saniyə qədər gözləyin |
| *"API ID və ya Hash yanlışdır"* | my.telegram.org-dan səhv kopyalama | Yenidən `/setup` yazın, diqqətlə kopyalayın |
| *"HuggingFace token yanlışdır"* | Səhv token və ya Read tipi | Write tipli yeni token yaradın |
| *"Space yaradıla bilmədi"* | HF xətası | `/setup` ilə yenidən cəhd edin |
| *"Session vaxtı bitdi"* | 10 dəqiqədən çox keçib | `/setup` yazıb yenidən başlayın |

---

### Addım 4 — Gözləyin və test edin

1. Bot sizə HuggingFace Space linkini verəcək
2. **İlk dəfə 3-7 dəqiqə gözləyin** (Docker build olur)
3. Telegram-da **istənilən söhbətə** `.alive` yazın
4. Cavab gəlsə — **bot işləyir!** 🎉

**`.alive` cavab vermirsə:**

1. HuggingFace Space linkinizi açın (bot verən link)
2. Vəziyyəti yoxlayın:

| Space statusu | Nə etməli |
|---------------|-----------|
| **Building** | Gözləyin, 3-7 dəqiqə çəkir |
| **Running** | Amma `.alive` cavab vermir → Settings → "Factory reboot" basın |
| **Runtime error** | Logs tabına baxın, xəta mesajını @apexsup qrupuna göndərin |
| **Sleeping** | Space linkinə klikləyin — oyanacaq (1-2 dəq gözləyin) |

---

## 🎮 Əsas Əmrlər

### Ümumi
| Əmr | Nə edir |
|-----|---------|
| `.alive` | Bot aktiv olub-olmadığını yoxlayır |
| `.help` | Bütün əmrlərin siyahısı |
| `.ping` | Cavab sürətini ölçür |
| `.restart` | Botu yenidən başladır |
| `.shutdown` | Botu söndürür |
| `.update` | Botu ən son versiyaya yeniləyir |

### Qrup idarəetmə
| Əmr | Nə edir |
|-----|---------|
| `.ban` | İstifadəçini qadağan edir (reply ilə) |
| `.unban` | Qadağanı ləğv edir |
| `.kick` | Qrupdan çıxarır |
| `.mute` | Susdurur |
| `.unmute` | Susdurmanı ləğv edir |
| `.promote` | Admin edir |
| `.demote` | Admin icazəsini ləğv edir |
| `.pin` | Mesajı sanclayır |

### Əyləncə & alətlər
| Əmr | Nə edir |
|-----|---------|
| `.song <ad>` | Musiqi axtarır və yükləyir |
| `.tr <dil> <mətn>` | Tərcümə edir (`.tr en salam`) |
| `.tts <mətn>` | Mətni səsə çevirir |
| `.carbon <kod>` | Kod-dan gözəl şəkil yaradır |
| `.afk <səbəb>` | AFK rejimini aktivləşdirir |
| `.sticker` | Şəkli stikerə çevirir |
| `.img <söz>` | Google-dan şəkil axtarır |
| `.weather <şəhər>` | Hava proqnozu göstərir |

### Database & backup
| Əmr | Nə edir |
|-----|---------|
| `.dbbackup` | Verilənlər bazasını BOTLOG qrupuna backup edir |
| `.dbrestore` | Son backup-dan bərpa edir |

### Plugin mağazası
| Əmr | Nə edir |
|-----|---------|
| `.store` | Mövcud pluginləri göstərir |
| `.install <ad>` | Plugin yükləyir |
| `.unload <ad>` | Plugini silir |

---

## ❓ Problemlər və Həlləri

### Bot `.alive`-a cavab vermir
1. Space linkinizi açın → status yoxlayın
2. **Building** → gözləyin
3. **Running** amma cavab yoxdur → Settings → **Factory reboot**
4. **Error** → Logs tabına baxın

### Bot dayanır / yatır
HuggingFace **pulsuz planda** Space 48 saat fəaliyyətsizlikdən sonra yatır.
- **Həll:** Space linkinə daxil olun — avtomatik oyanacaq (1-2 dəq)
- **Daimi həll:** HuggingFace-də ödənişli plan alın, və ya cron job ilə Space-i ayıq saxlayın

### "Database is locked" xətası
Bot çox əmri eyni anda icra etməyə çalışır.
- **Həll:** `.restart` yazın

### ".update" işləmir
- **Həll 1:** `.update now` yazın (zorla yeniləmə)
- **Həll 2:** HuggingFace Space → Settings → Factory reboot

### Plugin yüklədim amma işləmir
- Plugin versiyası uyğun olmaya bilər
- `.unload <plugin adı>` ilə silin
- `.restart` ilə botu yenidən başladın

### "FloodWaitError" — Telegram limit
Çox tez-tez əmr göndərmisiniz. Göstərilən müddət qədər gözləyin.

### Mesajlarım silinir / nəzarətsiz hərəkətlər
- Bəzi modullar avtomatik işləyir (blacklist, PM guard və s.)
- `.help` yazıb aktiv modulları yoxlayın
- Problemi tapandan sonra `.unload <modul>` ilə söndürün

### String Session nədir? Təhlükəlidirmi?
String Session — Telegram hesabınıza bot kimi qoşulmaq üçün açardır. O yalnız sizin HuggingFace Space-inizin **gizli dəyişənlərində** saxlanır. Heç kim (hətta Space yaradıcısı) onu görə bilməz.

### Botu tamamilə necə silim?
1. Telegram → Settings → Devices → "APEX" sessiyasını silin
2. [huggingface.co](https://huggingface.co) → Spaces → sizin space → Settings → **Delete this Space**

---

## 🔒 Təhlükəsizlik

- API ID/Hash — yalnız sizin HF Space-inizin secrets-ində
- String Session — yalnız HF secrets-ində, heç kim görə bilməz
- Setup Bot heç bir məlumatınızı saxlamır (qurulum bitdikdə silinir)
- Hesabınızı geri almaq: Telegram → Settings → Devices → lazımsız sessiyaları silin

---

## 🆘 Dəstək

Problem varsa: **@apexsup** qrupuna yazın.
