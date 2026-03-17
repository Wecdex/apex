# APEX Userbot - Update Module
# HuggingFace Space restart + git pull ile yenileme

import os
from userbot import LOGS, CMD_HELP
from userbot.events import register

HF_TOKEN = os.environ.get("HF_TOKEN", None)
HF_SPACE_ID = os.environ.get("HF_SPACE_ID", None)


@register(outgoing=True, pattern=r"^\.update(?: |$)")
async def update_bot(event):
    """Botu yenile — HF Space restart edir, git pull son kodu cekir."""

    if not HF_TOKEN or not HF_SPACE_ID:
        await event.edit(
            "`HF_TOKEN ve ya HF_SPACE_ID teyin edilmeyib.`\n"
            "`Bu emr yalniz HuggingFace-de isleyir.`"
        )
        return

    await event.edit("`Yenileme baslayir...\nDB backup alinir...`")

    # DB backup al (restart-dan evvel)
    try:
        from userbot.modules.db_backup import backup_db
        result = await backup_db(event.client)
        if result:
            await event.edit("`DB backup alindi.\nHF Space restart edilir...`")
        else:
            await event.edit("`DB backup alinmadi, amma davam edilir...\nHF Space restart edilir...`")
    except Exception as e:
        LOGS.warning(f"Update oncesi DB backup xetasi: {e}")
        await event.edit("`HF Space restart edilir...`")

    # HuggingFace Space restart
    try:
        from huggingface_hub import HfApi
        api = HfApi(token=HF_TOKEN)
        api.restart_space(HF_SPACE_ID)

        await event.edit(
            "`Yenileme ugurla basladi!`\n\n"
            "`HF Space restart edilir...`\n"
            "`Git pull ile son kod cekilecek.`\n"
            "`DB backup-dan berpa olunacaq.`\n\n"
            "`Bot 2-3 deqiqe erzinde yeniden aktivlesecek.`"
        )
    except Exception as e:
        LOGS.error(f"HF Space restart xetasi: {e}")
        await event.edit(
            f"`Yenileme xetasi!`\n`{e}`\n\n"
            "`HF_TOKEN ve HF_SPACE_ID-ni yoxlayin.`"
        )


CMD_HELP["update"] = """
**Bot Yenileme**

`.update` — Botu yenile (HuggingFace Space restart)

**Nece isleyir:**
1. DB backup alinir (BOTLOG qrupuna)
2. HF Space restart edilir
3. Git pull ile GitHub-dan son kod cekilir
4. DB backup-dan berpa olunur
5. Bot yeniden isleyir

**Qeyd:** Bu emr yalniz HuggingFace-de isleyir.
"""
