# U S Σ R Δ T O R / gsave (by Antigravity)

from telethon import events
from userbot import bot
from userbot.events import register
from userbot.cmdhelp import CmdHelp
import os

# Helper funksiya: Mesajdan kimin göndərdiyi, nə vaxt və hardan (qrup/kanal) olduğu məlumatını hazırlamaq
async def get_caption_info(target_msg, is_ttl=False):
    sender = await target_msg.get_sender()
    sender_name = "Naməlum"
    sender_user = "Yoxdur"
    
    if sender:
        sender_name = f"{getattr(sender, 'first_name', '')} {getattr(sender, 'last_name', '')}".strip() or "Naməlum"
        if getattr(sender, 'username', None):
            sender_user = f"@{sender.username}"

    date_str = target_msg.date.strftime("%Y-%m-%d %H:%M:%S")

    header = "📷 **TƏK DƏFƏLİK MEDİA XİLAS EDİLDİ!**\n\n" if is_ttl else "💾 **MEDİA XİLAS EDİLDİ!**\n\n"
    caption = (
        f"{header}"
        f"👤 **Göndərən:** {sender_name}\n"
        f"🔗 **İstifadəçi Adı:** {sender_user}\n"
        f"📅 **Tarix:** {date_str}"
    )
    return caption

# 1. Manul (Əllə) yadda saxlama tərəfi: .gsave komandası ilə (reply və ya link)
@register(outgoing=True, pattern=r"^\.gsave(?: |$)(.*)")
async def manual_save(event):
    if event.fwd_from:
        return
        
    await event.edit("`Gözləyin, yüklənir...`")
    link = event.pattern_match.group(1).strip()
    target_msg = None
    chat_id = None
    msg_id = None

    # Təyin edirik ki, reply-dir yoxsa link?
    if link:
        # Link formatı (məs: https://t.me/kanal_adi/1234)
        if "t.me/c/" in link: # gizli qrup linki
            # Özel qrupların link strukturu t.me/c/qrup_id/mesaj_id
            parts = link.split('/')
            try:
                chat_id = int(f"-100{parts[-2]}")
                msg_id = int(parts[-1])
            except:
                return await event.edit("`❌ Format səhvdir. Doğru gizli qrup linki daxil edin (t.me/c/id/msg_id).`")
        elif "t.me/" in link: # açıq qrup linki və ya kanal
            parts = link.split('/')
            try:
                chat_id = parts[-2]
                msg_id = int(parts[-1])
            except:
                 return await event.edit("`❌ Format səhvdir. Doğru ictimai link daxil edin.`")
        
        try:
           # Mesajı əldə edirik
           target_msgs = await event.client.get_messages(chat_id, ids=[msg_id])
           if not target_msgs or not target_msgs[0]:
                return await event.edit("`❌ Bu linkdəki mesaj tapılmadı. Ola bilsin o səhifəyə/qrupa üzv deyilsiniz.`")
           target_msg = target_msgs[0]
        except Exception as e:
           return await event.edit(f"`❌ Mesajı gətirərkən xəta yarandı:\nSəbəb: {str(e)}`")

    elif event.reply_to_msg_id:
        target_msg = await event.get_reply_message()
    else:
        return await event.edit("`❌ Mənə yükləməyim üçün bir medianı (reply edin) və ya onun linkini (.gsave <link>) verin!`")

    if not target_msg.media:
        return await event.edit("`❌ Bu mesajda şəkli və ya video yoxdur!`")

    # Album idarəçiliyi
    messages_to_save = []
    if target_msg.grouped_id:
        try:
             # Albomdursa o qrupdan həmin id-də olan digər mesajları da çəkirik
            from telethon.tl.types import InputMessagesFilterPhotos
            m_chat_id = chat_id if chat_id else event.chat_id
            
            # çox istək atmamaq ucun ehtiyat kimi limitləyirik (albom max 10 ola biler)
            async for album_msg in event.client.iter_messages(m_chat_id, limit=10, min_id=target_msg.id - 10, max_id=target_msg.id + 10):
                if album_msg.grouped_id == target_msg.grouped_id and album_msg.media:
                    messages_to_save.append(album_msg)
        except Exception as e:
            # Albom çıxarılmasa ən azı müraciət olunan əsas şəkli alaq
            messages_to_save = [target_msg]
    else:
        messages_to_save = [target_msg]

    try:
        # Mesajı(ları) endiririk -> Yadda Saxlanılan Mesajlara göndəririk (me)
        caption = await get_caption_info(target_msg)
        
        saved_files = []
        for msg in messages_to_save:
             dl_file = await event.client.download_media(message=msg.media)
             if dl_file:
                 saved_files.append(dl_file)
        
        if not saved_files:
            return await event.edit("`❌ Medianı yükləmək mümkün olmadı. Köməkçi fayl əldə edilmədi.`")
            
        await event.client.send_file(
            "me", 
            file=saved_files, 
            caption=caption
        )
        
        # Sonda uğurla bitdisə original postdakı gözləmə yazısını silək
        for f in saved_files:
             os.remove(f) # Yer tutmamaq üçün dərhal təmizləyirik (Telethon temp)

        await event.edit("`✅ Media 'Saved Messages' (Yadda saxlanılan mesajlar) bölməsinə göndərildi!`")
        
    except Exception as e:
        await event.edit(f"`❌ Medianı yükləmək baş tutmadı.\nXəta: {str(e)}`")

# 2. Avtomatik Tək Dəfəlik Media (TTL / Self-Destructing) qorunması
@bot.on(events.NewMessage)
async def ttl_saver(event):
    # Sadəcə gələn mesajlara baxır (özümüzün göndərdiklərindən qaçırıq)
    is_out_message = getattr(event, 'out', False) or (hasattr(event, 'message') and getattr(event.message, 'out', False))
    if is_out_message:
        return 
        
    try:
        media = getattr(event, 'media', None) or (hasattr(event, 'message') and getattr(event.message, 'media', None))
    except:
        media = None

    if not media:
        return

    # Şəklin və ya videonun "ttl_seconds" (baxılandan neçə saniyə sonra silinəcək) xüsusiyyəti varmı?
    has_ttl = False
    
    try:
        if hasattr(event.message.media, "ttl_seconds") and event.message.media.ttl_seconds is not None:
             has_ttl = True
        elif hasattr(event.media, "ttl_seconds") and event.media.ttl_seconds is not None:
             has_ttl = True
    except:
        pass

    if not has_ttl:
        return # Tək dəfəlik deyilsə çıxır
        
    # Əgər tək dəfəlik media aşkarlandısa səssizcə endir və Saved Mesajlara at
    try:
        # Faylı yüklə
        dl_file = await event.client.download_media(message=event.media)
        if dl_file:
            caption = await get_caption_info(event.message, is_ttl=True)
            await event.client.send_file(
                "me", 
                file=dl_file, 
                caption=caption
            )
            os.remove(dl_file) # sildik ki yer tutmasın

    except Exception as e:
        # Qarşı tərəfə HƏÇNƏ YAZILMIR! Xəta olsa sadəcə öz (Yadda saxlanılan) mesajlarına atılır
        try:
            sender_info = "Naməlum Şəxs"
            sender = await event.get_sender()
            if sender:
               sender_info = f"{getattr(sender, 'first_name', '')} (@{getattr(sender, 'username', 'yoxdur')})"
               
            err_msg = (
                f"🚨 **TƏK DƏFƏLİK MEDİA XƏTASI!**\n\n"
                f"👤 **Göndərən:** {sender_info}\n"
                f"Sizə göndərilən tək-dəfəlik görünən videonu/şəkli arxa planda yükləyib xilas etmək istərkən xəta baş verdi.\n\n"
                f"🛠 **Səbəb:** `{str(e)}`\n\n"
                f"_(Bu mesaj tamamilə məxfidir və o şəxsə getmir, ancaq sizin Saved Messages-ə göndərildi)._"
            )
            await event.client.send_message("me", err_msg)
        except:
             pass # Öz mesajlarımıza ata bilməsək heç nə etmirik (çata qarışvuruq)


CmdHelp('gsave').add_command(
    'gsave',
    '<link / reply>',
    'Xüsusi qruplardan yüklənə bilməyən şəkil və videoları .gsave yazaraq dərhal "Yadda saxlanılan mesajlar" bölmənizə yükləyin. Əlavə xüsusiyyət olaraq, kimsə sizə tək-dəfəlik görünən gizli (TTL) media atanda, bot avtomatik olaraq onu yükləyib xəlvətcə Saved Messages-ə atır (şəxsi söhbətə heçnə yazmır).'
).add()
