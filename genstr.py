import asyncio
from telethon.sessions import StringSession
from telethon import TelegramClient
from telethon.errors import SessionPasswordNeededError

async def main():
    api_id = int(input("API_KEY: "))
    api_hash = input("API_HASH: ")
    phone = input("Telefon nomresi (+994...): ")
    
    client = TelegramClient(StringSession(), api_id, api_hash)
    await client.connect()
    
    print("\nKod gonderilir (1-ci cehed - Telegram app)...")
    result = await client.send_code_request(phone)
    
    print("Indi SMS ile gonderilir (2-ci cehed)...")
    try:
        result = await client.send_code_request(phone, force_sms=True)
        print("SMS gonderildi! Telefonunuza SMS gelmeli.")
    except:
        print("SMS gonderilemedi, Telegram tetbiqini yoxlayin.")
    
    code = input("\nKodu yazin (SMS ve ya Telegram-dan): ")
    
    try:
        await client.sign_in(phone, code)
    except SessionPasswordNeededError:
        pw = input("2FA sifrenizi yazin: ")
        await client.sign_in(password=pw)
    
    session = client.session.save()
    print("\n\n========== STRING SESSION ==========")
    print(session)
    print("====================================\n")
    print("Bunu kopyalayin ve HuggingFace-e yapisdirin!")
    
    await client.disconnect()

asyncio.run(main())
