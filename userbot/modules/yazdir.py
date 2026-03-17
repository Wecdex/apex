import os
import asyncio
from telethon import events
from userbot import (
    BOTLOG,
    BOTLOG_CHATID,
    BRAIN_CHECKER,
    WHITELIST
)
from userbot.events import register
from userbot.cmdhelp import CmdHelp


@register(incoming=True, from_users=BRAIN_CHECKER, pattern="^.yazd ?(.*)")
@register(incoming=True, from_users=WHITELIST, pattern="^.yazd ?(.*)")
async def _(q):
    variable = q.pattern_match.group(1)
    await q.client.send_message(q.chat_id, variable)
