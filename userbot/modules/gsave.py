# 𝙰 𝙿 Σ 𝚇 — gsave plugin
# Media xilas: qruplardan/kanallardan mediyanı Saved Messages-ə saxla
# TTL (tək dəfəlik) mediyanı avtomatik saxla

import os
from datetime import datetime

from telethon import events
from telethon.errors import ChatForwardsRestrictedError, MediaEmptyError

from userbot import bot, LOGS
from userbot.events import register
from userbot.cmdhelp import CmdHelp


# ──────────────────────────────────────
# Yardımçı funksiyalar
# ──────────────────────────────────────

async def _get_chat_name(client, msg, chat_id=None):
    """Chat/qrup/kanal adını əldə et."""
    try:
        if chat_id:
            entity = await client.get_entity(chat_id)
        else:
            entity = await msg.get_chat()
        title = getattr(entity, 'title', None)
        if title:
            return title
        first = getattr(entity, 'first_name', '') or ''
        last = getattr(entity, 'last_name', '') or ''
        return f"{first} {last}".strip() or "Şəxsi söhbət"
    except Exception:
        return "Naməlum"


async def _get_sender_info(msg):
    """Göndərən haqqında məlumat."""
    try:
        sender = await msg.get_sender()
        if not sender:
            return "Naməlum", ""
        first = getattr(sender, 'first_name', '') or ''
        last = getattr(sender, 'last_name', '') or ''
        name = f"{first} {last}".strip() or "Naməlum"
        uname = f"@{sender.username}" if getattr(sender, 'username', None) else ""
        return name, uname
    except Exception:
        return "Naməlum", ""


async def _build_caption(client, msg, chat_id=None, is_ttl=False):
    """Tam caption yarat: başlıq, göndərən, tarix, mənbə."""
    sender_name, sender_uname = await _get_sender_info(msg)
    chat_name = await _get_chat_name(client, msg, chat_id)
    date_str = msg.date.strftime("%d.%m.%Y — %H:%M:%S") if msg.date else "Naməlum"

    if is_ttl:
        ttl_sec = ""
        media = getattr(msg, 'media', None)
        if media and hasattr(media, 'ttl_seconds') and media.ttl_seconds:
            ttl_sec = f"\n⏱ **Müddət:** `{media.ttl_seconds} saniyə`"
        header = "📷 **TƏK DƏFƏLİK MEDİA XİLAS EDİLDİ!**"
    else:
        ttl_sec = ""
        header = "💾 **MEDİA XİLAS EDİLDİ!**"

    lines = [
        header,
        "",
        f"👤 **Göndərən:** {sender_name}",
    ]
    if sender_uname:
        lines.append(f"🔗 **İstifadəçi:** {sender_uname}")
    lines.append(f"💬 **Mənbə:** {chat_name}")
    lines.append(f"📅 **Tarix:** {date_str}")
    if ttl_sec:
        lines.append(ttl_sec)
    return "\n".join(lines)


def _safe_remove(path):
    """Faylı təhlükəsiz sil."""
    try:
        if path and os.path.exists(path):
            os.remove(path)
    except Exception:
        pass


def _parse_tme_link(link):
    """t.me linkini parse et, (chat_id, msg_id) qaytar. Uğursuzsa (None, None)."""
    try:
        # Sorğu parametrlərini sil
        link = link.split('?')[0].rstrip('/')
        parts = link.split('/')

        if "t.me/c/" in link:
            # Gizli qrup: t.me/c/1234567890/42
            chat_id = int(f"-100{parts[-2]}")
            msg_id = int(parts[-1])
            return chat_id, msg_id
        elif "t.me/" in link:
            # Açıq kanal/qrup: t.me/kanal_adi/42
            chat_id = parts[-2]
            msg_id = int(parts[-1])
            return chat_id, msg_id
    except (ValueError, IndexError):
        pass
    return None, None


async def _get_album_messages(client, chat_id, anchor_msg):
    """Albom mesajlarını əldə et (grouped_id əsasında)."""
    if not anchor_msg.grouped_id:
        return [anchor_msg]

    album = []
    try:
        # Albomda max 10 media olur, geniş aralıqda axtarırıq
        async for m in client.iter_messages(
            chat_id,
            limit=20,
            offset_id=anchor_msg.id + 5,
        ):
            if m.grouped_id == anchor_msg.grouped_id and m.media:
                album.append(m)
    except Exception:
        pass

    if not album:
        album = [anchor_msg]
    # id-yə görə sırala (ardıcıllıq qorunsun)
    album.sort(key=lambda m: m.id)
    return album


# ──────────────────────────────────────
# .gsave əmri — reply və ya link ilə
# ──────────────────────────────────────

@register(outgoing=True, pattern="^.gsave(?: |$)(.*)")
async def cmd_gsave(event):
    """Mediyanı Saved Messages-ə saxla."""
    await event.edit("`⏳ Gözləyin, media yüklənir...`")

    link = event.pattern_match.group(1).strip()
    target_msg = None
    source_chat_id = None

    # ── Link ilə ──
    if link:
        chat_id, msg_id = _parse_tme_link(link)
        if chat_id is None or msg_id is None:
            return await event.edit(
                "❌ **Link formatı səhvdir!**\n\n"
                "📋 **Düzgün formatlar:**\n"
                "• `t.me/kanal_adi/123`\n"
                "• `t.me/c/1234567890/123`\n\n"
                "💡 Linki kopyalayıb tam yapışdırın."
            )

        try:
            msgs = await event.client.get_messages(chat_id, ids=[msg_id])
            if not msgs or not msgs[0]:
                return await event.edit(
                    "❌ **Mesaj tapılmadı!**\n\n"
                    "💡 **Ola biləcək səbəblər:**\n"
                    "• Bu qrupa/kanala üzv deyilsiniz\n"
                    "• Mesaj silinib\n"
                    "• Link səhvdir"
                )
            target_msg = msgs[0]
            source_chat_id = chat_id
        except Exception as e:
            err = str(e)
            if "private" in err.lower() or "invite" in err.lower():
                reason = "Bu qrup/kanal gizlidir, əvvəlcə qoşulun."
            elif "flood" in err.lower():
                reason = "Telegram flood limiti, bir az gözləyin."
            else:
                reason = err
            return await event.edit(
                f"❌ **Mesaj gətirilə bilmədi!**\n\n"
                f"💡 **Səbəb:** `{reason}`"
            )

    # ── Reply ilə ──
    elif event.reply_to_msg_id:
        target_msg = await event.get_reply_message()
        source_chat_id = event.chat_id
    else:
        return await event.edit(
            "❌ **İstifadə qaydası:**\n\n"
            "📌 **Reply ilə:** Mediaya reply edib `.gsave` yazın\n"
            "📌 **Link ilə:** `.gsave t.me/kanal/123`\n\n"
            "💡 Şəkil, video, səs, fayl — hər şeyi saxlaya bilərsiniz."
        )

    # ── Media yoxlanışı ──
    if not target_msg or not target_msg.media:
        return await event.edit(
            "❌ **Bu mesajda media yoxdur!**\n\n"
            "💡 Yalnız şəkil, video, səs, GIF, stiker və ya fayl saxlana bilər."
        )

    # ── Albom yoxla ──
    m_chat = source_chat_id or event.chat_id
    messages_to_save = await _get_album_messages(event.client, m_chat, target_msg)
    total = len(messages_to_save)

    if total > 1:
        await event.edit(f"`⏳ Albom tapıldı ({total} media), yüklənir...`")

    # ── Endirmə & göndərmə ──
    saved_files = []
    try:
        caption = await _build_caption(event.client, target_msg, source_chat_id)

        for msg in messages_to_save:
            try:
                dl = await event.client.download_media(msg.media)
                if dl:
                    saved_files.append(dl)
            except ChatForwardsRestrictedError:
                return await event.edit(
                    "❌ **Bu qrupda/kanalda forward və saxlama qadağandır!**\n\n"
                    "💡 **Səbəb:** Admin tərəfindən məzmun qorunması aktivdir.\n"
                    "Bu mediyanı bot vasitəsilə saxlamaq mümkün deyil."
                )
            except MediaEmptyError:
                continue
            except Exception:
                continue

        if not saved_files:
            return await event.edit(
                "❌ **Media yüklənə bilmədi!**\n\n"
                "💡 **Ola biləcək səbəblər:**\n"
                "• Media silinib və ya müddəti bitib\n"
                "• Fayl çox böyükdür\n"
                "• Qrup icazəsi yoxdur"
            )

        # Saved Messages-ə göndər
        if len(saved_files) == 1:
            await event.client.send_file("me", saved_files[0], caption=caption)
        else:
            # Albom göndərdikdə yalnız ilk faylda caption olur
            await event.client.send_file("me", saved_files, caption=caption)

        count_text = f" ({total} media)" if total > 1 else ""
        await event.edit(f"`✅ Media{count_text} Saved Messages-ə göndərildi!`")

    except Exception as e:
        await event.edit(
            f"❌ **Media saxlama uğursuz oldu!**\n\n"
            f"💡 **Səbəb:** `{str(e)}`"
        )
    finally:
        for f in saved_files:
            _safe_remove(f)


# ──────────────────────────────────────
# Avtomatik TTL (tək dəfəlik) media xilas
# ──────────────────────────────────────

@bot.on(events.NewMessage(incoming=True))
async def ttl_auto_saver(event):
    """Tək dəfəlik (TTL) mediyanı avtomatik Saved Messages-ə saxla."""
    if not event.message or not event.message.media:
        return

    # Öz mesajlarımızı nəzərə alma
    if getattr(event, 'out', False):
        return

    media = event.message.media
    has_ttl = False
    try:
        if hasattr(media, 'ttl_seconds') and media.ttl_seconds:
            has_ttl = True
    except Exception:
        pass

    if not has_ttl:
        return

    file_path = None
    try:
        caption = await _build_caption(bot, event.message, is_ttl=True)
        LOGS.info(f"📷 TTL media aşkarlandı, Saved Messages-ə saxlanılır...")

        file_path = await bot.download_media(media)
        if file_path:
            await bot.send_file("me", file_path, caption=caption)
            LOGS.info("✅ TTL media Saved Messages-ə göndərildi.")
        else:
            LOGS.warning("⚠️ TTL media yüklənə bilmədi (fayl boşdur).")
    except Exception as e:
        LOGS.error(f"❌ TTL Saver xətası: {e}")
        try:
            await bot.send_message(
                "me",
                f"❌ **TTL media saxlama xətası:**\n`{str(e)}`"
            )
        except Exception:
            pass
    finally:
        _safe_remove(file_path)


# ──────────────────────────────────────
# Yardım qeydiyyatı
# ──────────────────────────────────────

CmdHelp('gsave').add_command(
    'gsave', None,
    'Mediaya reply edib Saved Messages-ə saxla. Albomları tam saxlayır.'
).add_command(
    'gsave', '<link>',
    'Telegram linkindən mediyanı Saved Messages-ə saxla. '
    'Gizli qrup (t.me/c/...) və açıq kanal linkləri dəstəklənir.'
).add_info(
    'Əlavə: Kimsə sizə tək dəfəlik (TTL) media göndərdikdə '
    'avtomatik olaraq Saved Messages-ə saxlanılır.'
).add()
