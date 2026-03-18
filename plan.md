# APEX — İş Planı & Yaddaş

## ✅ Tamamlanan İşlər

### gsave.py — Tam yenidən yazıldı
- Pattern `^.gsave` — PATTERNS sistemi ilə uyğun
- Album handling düzəldildi (offset_id + grouped_id)
- Caption-da: göndərən, istifadəçi adı, mənbə chat adı, tarix
- TTL saver `@bot.on` ilə saxlanıldı (incoming üçün register uyğun deyil)
- `_safe_remove()` ilə təhlükəsiz fayl silmə
- `try/finally` ilə fayl cleanup
- `ChatForwardsRestrictedError` handle olunur
- CmdHelp ilə 2 əmr qeydiyyatdan keçdi + info əlavə edildi
- Hər xəta mesajı: aydın, səbəb göstərən, AZ dilində

### Bug Fixlər
- **__plugin.py**: pinstall tgbot yolunda `forward_to(PLUGIN_CHANNEL_ID)` əlavə edildi → plist-də görünür
- **events.py**: `BOTLOG_CHATID=0` olduqda `send_to=0` bug — `LOGSPAMMER and BOTLOG_CHATID` şərtinə dəyişdi
- **main.py**: `PLUGIN_CHANNEL_ID == None` → `is not None` düzəldildi
- **__init__.py**: inline bot GitHub linki `sahibziko/delta` → `Wecdex/apex`
- **__init__.py**: BOTLOG_CHATID=0 crash fix (quit→deaktiv), UPSTREAM_REPO_URL düzəlişi
- **Dil faylları**: AZ, DEFAULT, TR — `sahibziko/delta` → `Wecdex/apex`

### Setup Bot
- **setup_bot/bot.py**: BOT_TOKEN gizlədildi, BOTLOG logic düzəldildi
- **setup_bot/bot.py**: Bütün xəta mesajları ətraflılaşdırıldı (həm terminal həm user)
- **.gitignore**: setup_bot/ GitHub-a yüklənmir
- **git rm --cached setup_bot/**: tracking-dən silindi

### Help & Apex sistemi düzəldildi
- **__helpme.py** (.help / .yardım): inline bot olmadan da işləyir — text-based fallback
- **__up.py** (.apex): siyahı formatı düzəldildi (əvvəl elementlər atlanırdı, markdown qırıq idi)
- `.apex` — rəsmi modullar və yüklənmiş pluginlər ayrı göstərilir
- `.apex <ad>` — modul/plugin haqqında ətraflı məlumat
- `.apex <söz>` — təxmini axtarış (tam ad yazmağa ehtiyac yox)

### deyisdir.py — Tam yenidən yazıldı
- `.set` / `.deyisdir` / `.change` — sadə sintaksis, **tırnaq lazım deyil!**
- `.set` (boş) — bütün dəyişdirə biləcəyin mesajları + cari dəyərlərini göstərir
- `.set alive Salam dünya!` — birbaşa text ilə dəyişdir
- `.set afk` + reply — media və ya text ilə dəyişdir
- `.set alive` (tək) — cari dəyəri göstərir + istifadə təlimatı
- `.reset alive` — orijinala qaytar, `.reset all` — hamısını sıfırla
- 11 dəyişdirə bilən mesaj tipi: alive, afk, pm, kickme, ban, mute, approve, disapprove, block, restart, dızcı
- Bütün dəyişikliklər SQLite DB-də saxlanır — restart/space sönmə sonrası itmir

### misc.py — .restart düzəldildi
- Restart-dan əvvəl avtomatik DB backup alır
- BOTLOG mesajı try/except ilə qorunur

### update.py — Tam yenidən yazıldı
- `.update` — GitHub-dan yenilikləri yoxlayır, changelog göstərir (commit siyahısı + dəyişən fayllar)
- `.update now` — yenilikləri yüklə + bot restart (HF Space və ya local)
- Restart-dan əvvəl avtomatik DB backup
- HF Space varsa → Space restart (Dockerfile-dakı git pull işə düşür)
- HF yoxdursa → birbaşa git pull + execl restart
- upstream/origin fallback — git remote avtomatik idarə olunur

## ⚠️ Nəzərə Alınmalı
- `__plugin.py` pinstall-da `return os.remove(...)` — None qaytarır, funksional deyil amma pis stil
- db_backup.py BOTLOG deaktivdirsə backup/restore işləmir (dizayna uyğundur)
- gsave TTL saver `@bot.on` ilə qeydiyyat olunub — modul yükləndikdə aktiv olur

## 📋 Növbəti Potensial İşlər
- Əgər istifadəçi istəsə: gsave-ə batch save (birdəfəlik kanal/qrupdan çox media)
- Plugin store `@apexplugin` kanalının yenilənməsi
