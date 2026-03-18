# APEX Userbot
# SQLite DB Backup/Restore Sistemi

"""
Bot başlayanda BOTLOG_CHATID qrupundan son backup-ı bərpa edir.
Hər DB dəyişikliyindən sonra avtomatik backup göndərir (debounced).
Hər 1 saatda da mütləq backup göndərir.
.dbbackup əmri ilə manual backup almaq olar.
Bütün vaxtlar Bakı vaxtı (UTC+4) ilə göstərilir.
"""

import os
import asyncio
import datetime
from userbot import BOTLOG_CHATID, BOTLOG, LOGS, CMD_HELP, DB_URI
from userbot.events import register
from telethon.tl.types import InputMessagesFilterDocument

# Bakı vaxt zonası (UTC+4)
BAKU_TZ = datetime.timezone(datetime.timedelta(hours=4))

def baku_now():
    """Bakı vaxtını qaytar."""
    return datetime.datetime.now(BAKU_TZ)

# DB_URI-dən fayl path-ını avtomatik çıxart
if DB_URI and DB_URI.startswith("sqlite"):
    DB_PATH = DB_URI.split("///")[-1]
else:
    DB_PATH = "apex.db"

BACKUP_TAG = "#apexdb_backup"

# Debounce üçün: son planlanmış backup task
_pending_backup_task = None
_DEBOUNCE_SECONDS = 10  # 10 san gözlə, sonra backup göndər


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
    """DB faylını BOTLOG qrupuna göndərir (Bakı vaxtı ilə)."""
    if not BOTLOG or not BOTLOG_CHATID:
        return False

    if not os.path.exists(DB_PATH):
        LOGS.warning(f"{DB_PATH} faylı yoxdur!")
        return False

    try:
        now = baku_now().strftime("%Y-%m-%d %H:%M")
        await client.send_file(
            BOTLOG_CHATID,
            DB_PATH,
            caption=f"{BACKUP_TAG}\n📦 **DB Backup** — `{now}` (Bakı)",
        )
        return True
    except Exception as e:
        LOGS.warning(f"DB backup xətası: {e}")
        return False


async def _debounced_backup(client):
    """10 san gözlə, sonra backup göndər. Yeni commit gəlsə timer sıfırlanır."""
    await asyncio.sleep(_DEBOUNCE_SECONDS)
    result = await backup_db(client)
    if result:
        LOGS.info("DB dəyişikliyi sonrası avtomatik backup göndərildi ✅")


def schedule_backup():
    """DB commit-dən sonra çağırılır — 10 san debounce ilə backup planla.
    Bu funksiyanı sql_helper/__init__.py-dən çağırırıq."""
    global _pending_backup_task

    try:
        from userbot import bot
        if not bot or not BOTLOG or not BOTLOG_CHATID:
            return

        loop = bot.loop
        if loop is None or loop.is_closed():
            return

        # Əvvəlki planlanmış backup-ı ləğv et (debounce)
        if _pending_backup_task and not _pending_backup_task.done():
            _pending_backup_task.cancel()

        # Yeni backup planla
        _pending_backup_task = loop.create_task(_debounced_backup(bot))
    except Exception:
        pass


async def auto_backup_loop(client):
    """Hər 1 saatdan bir avtomatik backup göndərir."""
    while True:
        await asyncio.sleep(1 * 60 * 60)  # 1 saat
        result = await backup_db(client)
        if result:
            LOGS.info("Avtomatik saatlıq DB backup göndərildi ✅")


@register(outgoing=True, pattern=r"^.dbbackup(?: |$)")
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


@register(outgoing=True, pattern=r"^.dbrestore(?: |$)")
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

ℹ️ Hər DB dəyişikliyindən 10 san sonra avtomatik backup göndərilir.
ℹ️ Hər 1 saatda da mütləq backup göndərilir.
ℹ️ Bot restart olduqda son backup-dan data bərpa olunur.
ℹ️ Bütün vaxtlar Bakı vaxtı (UTC+4) ilə göstərilir.
"""
