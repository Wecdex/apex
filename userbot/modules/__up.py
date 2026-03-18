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

from userbot.cmdhelp import CmdHelp
from userbot import cmdhelp
from userbot import CMD_HELP, CMD_HELP_BOT, PATTERNS
from userbot.events import register

# ██████ LANGUAGE CONSTANTS ██████ #

from userbot.language import get_value
LANG = get_value("__up")

# ████████████████████████████████ #

@register(outgoing=True, pattern="^.apex(?: |$)(.*)")
async def apx(event):
    args = event.pattern_match.group(1).strip().lower()
    if args:
        if args in CMD_HELP:
            await event.edit(str(CMD_HELP[args]))
        else:
            # Təxmini uyğunluq: istifadəçi tam ad yazmaya bilər
            matches = [m for m in CMD_HELP if args in m]
            if len(matches) == 1:
                await event.edit(str(CMD_HELP[matches[0]]))
            elif len(matches) > 1:
                text = f"🔍 **\"{args}\" üçün nəticələr:**\n\n"
                for m in sorted(matches):
                    is_official = CMD_HELP_BOT.get(m, {}).get('info', {}).get('official', True)
                    icon = "📦" if is_official else "🔌"
                    text += f"{icon} `{m}`\n"
                text += f"\n💡 **İstifadə:** `{PATTERNS[:1]}apex <tam ad>`"
                await event.edit(text)
            else:
                await event.edit(
                    f"❌ **\"{args}\" adlı modul/plugin tapılmadı!**\n\n"
                    f"💡 Bütün modulları görmək üçün: `{PATTERNS[:1]}apex`\n"
                    f"💡 Axtarmaq üçün: `{PATTERNS[:1]}apex <söz>`"
                )
    else:
        # Modulları official / plugin olaraq ayır
        official = sorted([m for m in CMD_HELP if not m.startswith("_") and CMD_HELP_BOT.get(m, {}).get('info', {}).get('official', True)])
        plugins = sorted([m for m in CMD_HELP if not m.startswith("_") and not CMD_HELP_BOT.get(m, {}).get('info', {}).get('official', True)])
        hidden = sorted([m for m in CMD_HELP if m.startswith("_")])

        total = len(CMD_HELP)
        text = f"**✥ 𝙰 𝙿 Σ 𝚇 — Modullar ✥**\n\n"
        text += f"📦 **Ümumi:** `{total}` modul\n\n"

        if official:
            text += f"**� Rəsmi modullar ({len(official)}):**\n"
            for i in range(0, len(official), 3):
                row = official[i:i+3]
                text += "  ".join(f"`{m}`" for m in row) + "\n"
            text += "\n"

        if plugins:
            text += f"**🔌 Yüklənmiş pluginlər ({len(plugins)}):**\n"
            for i in range(0, len(plugins), 3):
                row = plugins[i:i+3]
                text += "  ".join(f"`{m}`" for m in row) + "\n"
            text += "\n"

        text += f"💡 **Ətraflı:** `{PATTERNS[:1]}apex <modul adı>`"
        await event.edit(text)
