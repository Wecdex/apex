# U S Σ R Δ T O R / Ümüd
# Yenidən yazıldı — sadə sintaksis, DB persist

import userbot.modules.sql_helper.mesaj_sql as sql
from userbot import CMD_HELP, PATTERNS
from userbot.events import register
from userbot.main import PLUGIN_MESAJLAR, ORJ_PLUGIN_MESAJLAR, PLUGIN_CHANNEL_ID
from userbot.cmdhelp import CmdHelp

# ═══════════════════════════════════════
# Dəyişdirə biləcəyiniz mesajlar + açıqlamaları
# ═══════════════════════════════════════

MESAJ_TURLERI = {
    "alive":      "🟢 .alive yazanda görünən mesaj",
    "afk":        "💤 AFK olduqda göstərilən mesaj",
    "pm":         "📩 İcazəsiz PM göndərənə cavab",
    "kickme":     "👋 Qrupdan çıxanda göstərilən mesaj",
    "ban":        "🔨 İstifadəçi banlandıqda mesaj",
    "mute":       "🔇 İstifadəçi susdurulduqda mesaj",
    "approve":    "✅ PM icazəsi verildikdə mesaj",
    "disapprove": "❌ PM icazəsi ləğv edildikdə mesaj",
    "block":      "🚫 İstifadəçi bloklandıqda mesaj",
    "restart":    "🔄 Bot yenidən başlayanda mesaj",
    "dızcı":      "🎨 Stiker oğurlayanda mesaj",
}


def _truncate(text, maxlen=40):
    """Uzun mesajları qısaldır."""
    if not text or not isinstance(text, str):
        return "(media/boş)"
    text = text.replace("\n", " ").strip()
    if len(text) > maxlen:
        return text[:maxlen] + "..."
    return text


# ═══════════════════════════════════════
# .set — mesajları dəyişdir
# ═══════════════════════════════════════

@register(outgoing=True, pattern=r"^\.set(?: |$)([\s\S]*)")
@register(outgoing=True, pattern=r"^\.deyisdir(?: |$)([\s\S]*)")
@register(outgoing=True, pattern=r"^\.change(?: |$)([\s\S]*)")
async def cmd_set(event):
    raw = event.pattern_match.group(1).strip()

    # ─── .set (boş) → siyahı göstər ───
    if not raw and not event.is_reply:
        text = "**⚙️ Dəyişdirə biləcəyiniz mesajlar:**\n\n"
        for key, desc in MESAJ_TURLERI.items():
            current = PLUGIN_MESAJLAR.get(key)
            is_custom = (current != ORJ_PLUGIN_MESAJLAR.get(key))
            mark = "✏️" if is_custom else "▪️"
            val = _truncate(current if isinstance(current, str) else None)
            text += f"{mark} **{key}** — {desc}\n"
            if is_custom:
                text += f"    └ `{val}`\n"
        text += (
            f"\n**İstifadə:**\n"
            f"`{PATTERNS[:1]}set alive Mən aktivəm! 🚀`\n"
            f"`{PATTERNS[:1]}set afk` ← mediaya reply et\n"
            f"`{PATTERNS[:1]}reset alive` ← orijinala qaytar\n"
            f"`{PATTERNS[:1]}reset all` ← hamısını sıfırla"
        )
        return await event.edit(text)

    # ─── Tip + mesaj ayır ───
    parts = raw.split(None, 1)
    tip = parts[0].lower() if parts else ""
    mesaj_text = parts[1].strip() if len(parts) > 1 else ""

    # ─── Tip yoxlaması ───
    if tip not in MESAJ_TURLERI:
        available = ", ".join(f"`{k}`" for k in MESAJ_TURLERI)
        return await event.edit(
            f"❌ **\"{tip}\" tanınmır!**\n\n"
            f"Dəyişdirə biləcəkləriniz:\n{available}"
        )

    # ─── Reply ilə dəyişdirmə (media və ya text) ───
    if event.is_reply and not mesaj_text:
        reply = await event.get_reply_message()
        if reply.media:
            try:
                forwarded = await reply.forward_to(PLUGIN_CHANNEL_ID)
                PLUGIN_MESAJLAR[tip] = reply
                sql.ekle_mesaj(tip, f"MEDYA_{forwarded.id}")
                return await event.edit(
                    f"✅ **{tip}** mesajı mediaya dəyişdirildi!\n"
                    f"ℹ️ DB-də saxlanıldı, restart-dan sonra da qalacaq."
                )
            except Exception as e:
                return await event.edit(f"❌ Media saxlanarkən xəta: `{e}`")
        elif reply.text:
            PLUGIN_MESAJLAR[tip] = reply.text
            sql.ekle_mesaj(tip, reply.text)
            return await event.edit(
                f"✅ **{tip}** mesajı dəyişdirildi!\n"
                f"📝 `{_truncate(reply.text, 60)}`\n"
                f"ℹ️ DB-də saxlanıldı."
            )
        else:
            return await event.edit("❌ Reply olunan mesajda text və ya media yoxdur.")

    # ─── Text ilə dəyişdirmə (.set alive Salam dünya!) ───
    if mesaj_text:
        PLUGIN_MESAJLAR[tip] = mesaj_text
        sql.ekle_mesaj(tip, mesaj_text)
        return await event.edit(
            f"✅ **{tip}** mesajı dəyişdirildi!\n"
            f"📝 `{_truncate(mesaj_text, 60)}`\n"
            f"ℹ️ DB-də saxlanıldı."
        )

    # ─── .set alive (mesaj yox, reply yox) → cari dəyəri göstər ───
    current = PLUGIN_MESAJLAR.get(tip)
    is_custom = (current != ORJ_PLUGIN_MESAJLAR.get(tip))
    val = _truncate(current if isinstance(current, str) else None, 80)
    status = "✏️ Dəyişdirilib" if is_custom else "▪️ Orijinal"
    return await event.edit(
        f"**⚙️ {tip}** — {MESAJ_TURLERI[tip]}\n\n"
        f"**Status:** {status}\n"
        f"**Cari dəyər:** `{val}`\n\n"
        f"**Dəyişdirmək üçün:**\n"
        f"`{PATTERNS[:1]}set {tip} Yeni mesaj buraya`\n"
        f"**və ya** mediaya reply edib `{PATTERNS[:1]}set {tip}` yazın\n"
        f"**Sıfırlamaq üçün:** `{PATTERNS[:1]}reset {tip}`"
    )


# ═══════════════════════════════════════
# .reset — orijinala qaytar
# ═══════════════════════════════════════

@register(outgoing=True, pattern=r"^\.reset(?: |$)(.*)")
async def cmd_reset(event):
    tip = event.pattern_match.group(1).strip().lower()

    if not tip:
        return await event.edit(
            f"**🔄 Mesajı orijinala qaytarmaq üçün:**\n"
            f"`{PATTERNS[:1]}reset alive` — alive mesajını sıfırla\n"
            f"`{PATTERNS[:1]}reset all` — hamısını sıfırla"
        )

    # ─── Hamısını sıfırla ───
    if tip == "all":
        count = 0
        for key in MESAJ_TURLERI:
            if PLUGIN_MESAJLAR.get(key) != ORJ_PLUGIN_MESAJLAR.get(key):
                PLUGIN_MESAJLAR[key] = ORJ_PLUGIN_MESAJLAR[key]
                sql.sil_mesaj(key)
                count += 1
        return await event.edit(
            f"✅ **{count}** mesaj orijinala qaytarıldı!\n"
            f"ℹ️ DB-dən silindi."
        )

    # ─── Tip yoxlaması ───
    if tip not in MESAJ_TURLERI:
        available = ", ".join(f"`{k}`" for k in MESAJ_TURLERI)
        return await event.edit(
            f"❌ **\"{tip}\" tanınmır!**\n\n"
            f"Sıfırlaya biləcəkləriniz:\n{available}"
        )

    # ─── Tək mesajı sıfırla ───
    result = sql.sil_mesaj(tip)
    PLUGIN_MESAJLAR[tip] = ORJ_PLUGIN_MESAJLAR[tip]
    if result is True:
        return await event.edit(
            f"✅ **{tip}** mesajı orijinala qaytarıldı!\n"
            f"ℹ️ DB-dən silindi."
        )
    else:
        return await event.edit(
            f"⚠️ **{tip}** artıq orijinaldadır (dəyişdirilməyib)."
        )


# ═══════════════════════════════════════
# CmdHelp
# ═══════════════════════════════════════

CmdHelp('deyisdir').add_command(
    'set', '<tip> <mesaj>',
    'Bot mesajlarını dəyişdir. Tırnaq lazım deyil! Mediaya reply etmək də olar.',
    'set alive Mən aktivəm! 🚀'
).add_command(
    'reset', '<tip>',
    'Mesajı orijinala qaytar. .reset all — hamısını sıfırla.',
    'reset alive'
).add_info(
    'Bot mesajlarını (alive, afk, ban, mute...) dəyişdir və ya sıfırla. Dəyişikliklər DB-də saxlanır.'
).add()
