# Copyright (C) 2020 U S Σ R Δ T O R
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
#

from userbot import BOT_USERNAME, CMD_HELP, PATTERNS
from userbot.events import register

# ██████ LANGUAGE CONSTANTS ██████ #

from userbot.language import get_value
LANG = get_value("__helpme")

# ████████████████████████████████ #

@register(outgoing=True, pattern="^.yard[iı]m|^.help")
async def yardim(event):
    tgbotusername = BOT_USERNAME
    if tgbotusername is not None:
        try:
            results = await event.client.inline_query(
                tgbotusername,
                "@ApexUserbot"
            )
            await results[0].click(
                event.chat_id,
                reply_to=event.reply_to_msg_id,
                hide_via=True
            )
            await event.delete()
            return
        except Exception:
            pass

    # Inline bot yoxdursa və ya işləmirsə — text-based help
    modules = sorted([m for m in CMD_HELP if not m.startswith("_")])
    total = len(modules)

    text = (
        "**✥ 𝙰 𝙿 Σ 𝚇 — Yardım ✥**\n\n"
        f"📦 **Yüklənən modul sayı:** `{total}`\n\n"
    )

    for i in range(0, len(modules), 3):
        row = modules[i:i+3]
        text += "  ".join(f"`{m}`" for m in row) + "\n"

    text += (
        f"\n💡 **İstifadə:** `{PATTERNS[:1]}apex <modul adı>`\n"
        f"📖 **Məsələn:** `{PATTERNS[:1]}apex gsave`"
    )
    await event.edit(text)
