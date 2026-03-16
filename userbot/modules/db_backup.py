# U S Σ R Δ T O R
# SQLite DB Backup/Restore Sistemi

"""
Bot başlayanda BOTLOG_CHATID qrupundan son backup-ı bərpa edir.
Hər 6 saatda avtomatik backup göndərir.
.dbbackup əmri ilə manual backup almaq olar.
"""

import os
import asyncio
import datetime
from userbot import BOTLOG_CHATID, BOTLOG, LOGS, CMD_HELP
from userbot.events import register
from telethon.tl.types import InputMessagesFilterDocument

DB_PATH = "dto.db"
BACKUP_TAG = "#dtodb_backup"


async def restore_db(client):
    """Bot başlayanda BOTLOG qrupundan son backup-ı bərpa edir."""
    if not BOTLOG or not BOTLOG_CHATID:
        LOGS.info("BOTLOG aktiv deyil, DB restore atlanır.")
        return False

    try:
        LOGS.info("BOTLOG qrupundan son DB backup axtarılır...")
        async for msg in client.iter_messages(
            BOTLOG_CHATID,
            filter=InputMessagesFilterDocument,
            search=BACKUP_TAG,
            limit=5
        ):
            if msg.file and msg.file.name and msg.file.name.endswith(".db"):
                LOGS.info(f"DB backup tapıldı (ID: {msg.id}), yüklənir...")
                await client.download_media(msg, DB_PATH)
                LOGS.info("DB uğurla bərpa edildi! ✅")
                return True

        LOGS.info("Heç bir DB backup tapılmadı, boş DB ilə başlanır.")
        return False
    except Exception as e:
        LOGS.warning(f"DB restore xətası: {e}")
        return False


async def backup_db(client):
    """dto.db faylını BOTLOG qrupuna göndərir."""
    if not BOTLOG or not BOTLOG_CHATID:
        return False

    if not os.path.exists(DB_PATH):
        LOGS.warning("dto.db faylı yoxdur!")
        return False

    try:
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        await client.send_file(
            BOTLOG_CHATID,
            DB_PATH,
            caption=f"{BACKUP_TAG}\n📦 **DB Backup** — `{now}`",
        )
        return True
    except Exception as e:
        LOGS.warning(f"DB backup xətası: {e}")
        return False


async def auto_backup_loop(client):
    """Hər 6 saatda avtomatik backup göndərir."""
    while True:
        await asyncio.sleep(6 * 60 * 60)  # 6 saat
        result = await backup_db(client)
        if result:
            LOGS.info("Avtomatik DB backup göndərildi ✅")


@register(outgoing=True, pattern=r"^.dbbackup$")
async def manual_backup(event):
    """Manual DB backup əmri."""
    msg = await event.edit("`DB backup hazırlanır...`")
    
    if not BOTLOG:
        return await msg.edit("`❌ Backup alınmadı: BOTLOG dəyişkəni False olaraq ayarlanmışdır.`\n`HuggingFace quraşdırmalarında BOTLOG=True olmalıdır.`")
        
    if not BOTLOG_CHATID:
        return await msg.edit("`❌ Backup alınmadı: BOTLOG_CHATID dəyişkəni yoxdur və ya səhvdir.`")
        
    result = await backup_db(event.client)
    if result:
        await msg.edit("`DB backup uğurla gönderildi! ✅`\n`Bax: BOTLOG qrupu`")
    else:
        await msg.edit("`DB backup göndərilə bilmədi! ❌ Ola bilər ki, botun BOTLOG qrupuna mesaj yazma icazəsi yoxdur.`")


@register(outgoing=True, pattern=r"^.dbrestore$")
async def manual_restore(event):
    """Manual DB restore əmri."""
    msg = await event.edit("`DB bərpa edilir...`")
    result = await restore_db(event.client)
    if result:
        await msg.edit("`DB uğurla bərpa edildi! ✅ Bot yenidən başladılmalıdır.`")
    else:
        await msg.edit("`Heç bir backup tapılmadı! ❌`")


CMD_HELP["db_backup"] = """
📦 **DB Backup Sistemi**

`.dbbackup` — Database-i BOTLOG qrupuna backup edir
`.dbrestore` — BOTLOG qrupundan son backup-ı bərpa edir

ℹ️ Bot avtomatik olaraq hər 6 saatda backup göndərir.
ℹ️ Bot restart olduqda son backup-dan data bərpa olunur.
"""
