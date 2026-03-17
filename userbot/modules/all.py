import os
from telethon import events
from userbot.events import register

@register(outgoing=True, pattern=r'^\.py (\w+)$')
async def convert_to_py(event):
    # Fayl adı təyin edirik (bu halda, "salam" fayl adı olacaq)
    filename = event.pattern_match.group(1) + ".py"
    
    # Mesajın cavabını alırıq
    reply = await event.get_reply_message()
    
    if not reply:
        await event.edit("`Faylı cavablandırın və əmri verin.`")
        return
    
    # Cavab verilmiş mesajın məzmununu götürürük
    script_content = reply.text
    
    if not script_content:
        await event.edit("`Verilən mesajda heç bir məzmun yoxdur.`")
        return
    
    # Fayl adını və məzmunu yazırıq
    try:
        with open(filename, "w") as file:
            file.write(script_content)
        
        # Faylı Telegram-a göndəririk
        await event.reply(file=filename)
        await event.edit(f"Fayl `{filename}` yaradıldı və göndərildi.")
        
        # Faylın silinməsi
        os.remove(filename)
    
    except Exception as e:
        await event.edit(f"Fayl yaradılarkən xəta baş verdi: {str(e)}")