# @apexuserbot
# @hus3ynx

import asyncio
import random
from userbot.events import register
from userbot import bot
import os
from userbot.cmdhelp import CmdHelp

@register(pattern="^.esq ?(.*)", outgoing=True)
async def esq(event):
    me = await bot.get_me()
    await event.edit(f'`{random.choice(["❤️", "🧡," "💛", "💚", "💙", "💜", "🖤"])} Eşq faizi hesablanır...`')

    if event.is_reply:
        reply = await event.get_reply_message()
        reply_user = await event.client.get_entity(reply.from_id)
        text = event.pattern_match.group(1)

        if text == '':
            firstUser_id = me.id
            if me.username:
                firstUser = f'@{me.username}'
            else:
                firstUser = f'[{me.first_name}](tg://user?id={me.id})'
        else:
            if '?id' in text:
                firstUser_id = text.split('?id=')[1]
            else:
                firstUser_id = text
            firstUser = text

        if reply_user.username:
            secondUser_id = reply_user.id
            secondUser = f'@{reply_user.username}'
        else:
            secondUser_id = reply_user.id
            secondUser = f'[{reply_user.first_name}](tg://user?id={reply_user.id})'
    else:
        return await event.edit('`Zəhmət olmasa bir istifadəçiyə yanıt verin.`')

    for i in range(0,10):
        await event.edit(f'`{random.choice(["❤️", "🧡" "💛", "💚", "💙", "💜", "🖤"])} Eşq faizi hesablanır... %{random.randint(0, 100)}`')
        await asyncio.sleep(0.3)
        
    if os.path.exists(f'{firstUser_id}-{secondUser_id}.txt'):
        faiz = open(f'{firstUser_id}-{secondUser_id}.txt', 'r').read()
        await event.edit(f'{firstUser} `ilə` {secondUser} `arasındakı eşq hesablandı!`\n**Nəticə:** `%{faiz}`')
    else:
        faiz = random.randint(0, 100)
        open(f'{firstUser_id}-{secondUser_id}.txt', 'a+').write(str(faiz))
        await event.edit(f'{firstUser} `ilə` {secondUser} `arasındakı eşq hesablandı!`\n**Nəticə:** `%{faiz}`')

CmdHelp('esq').add_command(
    'Esq', '<birinci istifadəçi/yanıt> <ikinci istifadəçi/siz>', 'Yanıt verdiyiviz vəya nickini verdiyiniz istifadəçi ilə sizin vəya ikinci istifadəçi arasındaki eşq faizini ölçər!'
).add_info('@hus3ynx və @thisisulvis tərəfindən hazırlanmışdır.').add()