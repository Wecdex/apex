#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
APEX Userbot - Setup Bot
Telegram vasitesile avtomatik userbot qurulumu

Istifadeciler bu bot vasitesile:
1. STRING_SESSION yaradir
2. HuggingFace Space acir
3. Userbotu avtomatik qurasdirir
"""

import os
import logging
import http.server
import threading
import tempfile
import time
import subprocess
from telegram import Update
from telegram.ext import (
    Application, CommandHandler, MessageHandler,
    ConversationHandler, filters, ContextTypes
)
from telethon import TelegramClient
from telethon.sessions import StringSession
from telethon.errors import (
    SessionPasswordNeededError, PhoneNumberInvalidError,
    PhoneCodeInvalidError, PasswordHashInvalidError,
    FloodWaitError, ApiIdInvalidError
)
from telethon.tl.functions.channels import CreateChannelRequest
from huggingface_hub import HfApi

# ==========================================
# KONFIQURASIYA
# ==========================================
BOT_TOKEN = os.environ.get("SETUP_BOT_TOKEN", "8627242727:AAF97myd1Yfw6PBK27u-Gu3s-3v43JfpCRs")
GITHUB_REPO = os.environ.get("GITHUB_REPO", "https://github.com/sahibziko/delta")

logging.basicConfig(
    format="%(asctime)s - APEX Setup - %(levelname)s - %(message)s",
    level=logging.INFO,
)
log = logging.getLogger(__name__)

# Conversation states
ASK_API_ID, ASK_API_HASH, ASK_PHONE, ASK_CODE, ASK_2FA, ASK_HF_TOKEN = range(6)

# ==========================================
# DOCKERFILE TEMPLATE (istifadecinin Space-i ucun)
# ==========================================
USERBOT_DOCKERFILE = """FROM python:3.11-slim

RUN apt-get update && apt-get install -y \\
    git ffmpeg libcairo2-dev \\
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

RUN git clone {repo}.git .

RUN pip install --no-cache-dir -r requirements.txt || true

EXPOSE 7860

CMD ["bash", "-c", "git pull origin main 2>/dev/null || true; python3 app.py"]
"""


# ==========================================
# HEALTH CHECK SERVER (HuggingFace ucun)
# ==========================================
class HealthHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(
            b"<h1>APEX Setup Bot</h1><p>Bot is running. Talk to it on Telegram.</p>"
        )

    def log_message(self, format, *args):
        pass


def start_health_server():
    server = http.server.HTTPServer(("0.0.0.0", 7860), HealthHandler)
    t = threading.Thread(target=server.serve_forever, daemon=True)
    t.start()
    log.info("Health server started on port 7860")


# ==========================================
# YARDIMCI FONKSIYALAR
# ==========================================
async def cleanup_client(context: ContextTypes.DEFAULT_TYPE):
    client = context.user_data.get("client")
    if client:
        try:
            if client.is_connected():
                await client.disconnect()
        except Exception:
            pass
    context.user_data.pop("client", None)


# ==========================================
# /start
# ==========================================
async def cmd_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await cleanup_client(context)
    context.user_data.clear()

    text = (
        "<b>APEX Userbot Qurulum Botu</b>\n\n"
        "Bu bot size <b>5 deqiqe</b> erzinde pulsuz Telegram userbot qurmaga komek edecek.\n\n"
        "<b>Lazim olanlar:</b>\n"
        "1. Telegram API melumatlari - <a href='https://my.telegram.org/auth'>my.telegram.org</a>\n"
        "2. HuggingFace hesabi - <a href='https://huggingface.co/join'>huggingface.co</a>\n\n"
        "Hazir olduqda /setup yazin."
    )
    await update.message.reply_text(
        text, parse_mode="HTML", disable_web_page_preview=True
    )


# ==========================================
# /setup - Quruluma basla
# ==========================================
async def cmd_setup(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await cleanup_client(context)
    context.user_data.clear()

    text = (
        "<b>Addim 1/6 - API ID</b>\n\n"
        "1. <a href='https://my.telegram.org/auth'>my.telegram.org</a> saytina daxil olun\n"
        "2. <b>API development tools</b> bolmesine kecin\n"
        "3. <code>api_id</code> (reqem) kopyalayib gonderin\n\n"
        "<b>API ID gonderin:</b>"
    )
    await update.message.reply_text(
        text, parse_mode="HTML", disable_web_page_preview=True
    )
    return ASK_API_ID


# ==========================================
# Addim 1: API ID
# ==========================================
async def step_api_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        api_id = int(update.message.text.strip())
    except ValueError:
        await update.message.reply_text("API ID reqem olmalidir. Yeniden gonderin:")
        return ASK_API_ID

    context.user_data["api_id"] = api_id

    text = (
        "<b>Addim 2/6 - API Hash</b>\n\n"
        "Eyni sehifeden <code>api_hash</code> kopyalayib gonderin.\n"
        "(32 simvolluq metn)\n\n"
        "<b>API Hash gonderin:</b>"
    )
    await update.message.reply_text(text, parse_mode="HTML")
    return ASK_API_HASH


# ==========================================
# Addim 2: API Hash
# ==========================================
async def step_api_hash(update: Update, context: ContextTypes.DEFAULT_TYPE):
    api_hash = update.message.text.strip()
    if len(api_hash) != 32:
        await update.message.reply_text(
            f"API Hash 32 simvol olmalidir (sizinki {len(api_hash)}). Yeniden gonderin:"
        )
        return ASK_API_HASH

    context.user_data["api_hash"] = api_hash

    text = (
        "<b>Addim 3/6 - Telefon Nomresi</b>\n\n"
        "Telegram hesabinizin telefon nomresini beynelxalq formatda yazin.\n"
        "Meselen: <code>+994501234567</code>\n\n"
        "<b>Telefon nomresi gonderin:</b>"
    )
    await update.message.reply_text(text, parse_mode="HTML")
    return ASK_PHONE


# ==========================================
# Addim 3: Telefon + Kod gonder
# ==========================================
async def step_phone(update: Update, context: ContextTypes.DEFAULT_TYPE):
    phone = update.message.text.strip()
    if not phone.startswith("+"):
        phone = "+" + phone

    context.user_data["phone"] = phone
    await update.message.reply_text("Telegram-a qosulur, kod gonderilir...")

    try:
        client = TelegramClient(
            StringSession(),
            context.user_data["api_id"],
            context.user_data["api_hash"],
        )
        await client.connect()

        sent = await client.send_code_request(phone)
        context.user_data["client"] = client
        context.user_data["phone_code_hash"] = sent.phone_code_hash

        text = (
            "<b>Addim 4/6 - Tesdiq Kodu</b>\n\n"
            "Telegram-dan size <b>5 reqemli kod</b> geldi.\n\n"
            "Tehlukesizlik ucun kodu <b>bosluqlarla</b> ayirin:\n"
            "Meselen: <code>1 2 3 4 5</code>\n\n"
            "<b>Kodu gonderin:</b>"
        )
        await update.message.reply_text(text, parse_mode="HTML")
        return ASK_CODE

    except PhoneNumberInvalidError:
        await update.message.reply_text(
            "Telefon nomresi yanlisdir! Yeniden gonderin:"
        )
        return ASK_PHONE
    except ApiIdInvalidError:
        await cleanup_client(context)
        await update.message.reply_text(
            "API ID ve ya API Hash yanlisdir!\n/setup yazaraq yeniden baslayin."
        )
        return ConversationHandler.END
    except FloodWaitError as e:
        await cleanup_client(context)
        await update.message.reply_text(
            f"Telegram flood limit! {e.seconds} saniye gozleyin ve /setup yazin."
        )
        return ConversationHandler.END
    except Exception as e:
        await cleanup_client(context)
        await update.message.reply_text(
            f"Xeta: {e}\n\nTelefon nomresini yeniden gonderin:"
        )
        return ASK_PHONE


# ==========================================
# Addim 4: Kod ile giris
# ==========================================
async def step_code(update: Update, context: ContextTypes.DEFAULT_TYPE):
    code = update.message.text.strip().replace(" ", "").replace("-", "")
    client = context.user_data.get("client")

    if not client:
        await update.message.reply_text(
            "Session vaxti bitdi. /setup yazaraq yeniden baslayin."
        )
        return ConversationHandler.END

    try:
        await client.sign_in(
            context.user_data["phone"],
            code,
            phone_code_hash=context.user_data["phone_code_hash"],
        )

        # Ugurlu giris
        session_string = client.session.save()
        context.user_data["session"] = session_string
        await update.message.reply_text("Telegram giris ugurlu!")

        # BOTLOG qrupu yarat
        await _create_botlog(update, context, client)

        await client.disconnect()
        context.user_data.pop("client", None)

        # HuggingFace addimina kec
        return await _ask_hf_token(update)

    except SessionPasswordNeededError:
        text = (
            "<b>Addim 4.5 - Iki Faktorlu Tesdiq (2FA)</b>\n\n"
            "Hesabinizda 2FA aktivdir.\n"
            "2FA sifrenizi gonderin:\n\n"
            "<b>Sifre:</b>"
        )
        await update.message.reply_text(text, parse_mode="HTML")
        return ASK_2FA

    except PhoneCodeInvalidError:
        await update.message.reply_text("Kod yanlisdir! Yeniden gonderin:")
        return ASK_CODE

    except Exception as e:
        await cleanup_client(context)
        await update.message.reply_text(
            f"Xeta: {e}\n/setup yazaraq yeniden baslayin."
        )
        return ConversationHandler.END


# ==========================================
# Addim 4.5: 2FA sifre
# ==========================================
async def step_2fa(update: Update, context: ContextTypes.DEFAULT_TYPE):
    password = update.message.text.strip()
    client = context.user_data.get("client")

    if not client:
        await update.message.reply_text(
            "Session vaxti bitdi. /setup yazaraq yeniden baslayin."
        )
        return ConversationHandler.END

    try:
        await client.sign_in(password=password)

        session_string = client.session.save()
        context.user_data["session"] = session_string
        await update.message.reply_text("2FA giris ugurlu!")

        # BOTLOG qrupu yarat
        await _create_botlog(update, context, client)

        await client.disconnect()
        context.user_data.pop("client", None)

        # HuggingFace addimina kec
        return await _ask_hf_token(update)

    except PasswordHashInvalidError:
        await update.message.reply_text("2FA sifre yanlisdir! Yeniden gonderin:")
        return ASK_2FA
    except Exception as e:
        await cleanup_client(context)
        await update.message.reply_text(
            f"Xeta: {e}\n/setup yazaraq yeniden baslayin."
        )
        return ConversationHandler.END


# ==========================================
# BOTLOG qrupu yaratma
# ==========================================
async def _create_botlog(update, context, client):
    await update.message.reply_text("BOTLOG qrupu yaradilir...")
    try:
        result = await client(
            CreateChannelRequest(
                title="APEX Botlog",
                about="APEX Userbot - Logs & DB Backup",
                megagroup=True,
            )
        )
        channel = result.chats[0]
        context.user_data["botlog_chatid"] = int(f"-100{channel.id}")
        await update.message.reply_text("BOTLOG qrupu yaradildi!")
    except Exception as e:
        log.warning(f"BOTLOG yaradila bilmedi: {e}")
        context.user_data["botlog_chatid"] = 0
        await update.message.reply_text(
            "BOTLOG qrupu avtomatik yaradila bilmedi.\n"
            "Bot qurulduqdan sonra manual yarada bilersiniz."
        )


# ==========================================
# HuggingFace token sorgusu
# ==========================================
async def _ask_hf_token(update):
    text = (
        "<b>Addim 5/6 - HuggingFace Token</b>\n\n"
        "1. <a href='https://huggingface.co/join'>huggingface.co</a> saytinda hesab acin\n"
        "2. <a href='https://huggingface.co/settings/tokens'>Token sehifesine</a> kecin\n"
        "3. <b>Create new token</b> basin\n"
        "   - Ad: <code>apex</code>\n"
        "   - Type: <b>Write</b>\n"
        "4. Token-i kopyalayib gonderin\n\n"
        "<b>HuggingFace token gonderin:</b>"
    )
    await update.message.reply_text(
        text, parse_mode="HTML", disable_web_page_preview=True
    )
    return ASK_HF_TOKEN


# ==========================================
# Addim 5: HuggingFace Token + Space yaratma
# ==========================================
async def step_hf_token(update: Update, context: ContextTypes.DEFAULT_TYPE):
    token = update.message.text.strip()

    await update.message.reply_text("HuggingFace token yoxlanilir...")

    # Token validation
    try:
        api = HfApi(token=token)
        user_info = api.whoami()
        hf_username = user_info["name"]
    except Exception:
        await update.message.reply_text(
            "HuggingFace token yanlisdir!\n"
            "Token <code>hf_...</code> ile baslamalidir.\n\n"
            "Yeniden gonderin:",
            parse_mode="HTML",
        )
        return ASK_HF_TOKEN

    await update.message.reply_text(
        f"HF hesab: <b>{hf_username}</b>\n\n"
        "<b>Addim 6/6 - Space yaradilir...</b>\n"
        "Bu 1-2 deqiqe ceke biler. Gozleyin...",
        parse_mode="HTML",
    )

    repo_id = f"{hf_username}/apex-userbot"

    try:
        # 1. Space yarat
        try:
            api.create_repo(
                repo_id=repo_id,
                repo_type="space",
                space_sdk="docker",
                private=False,
            )
            log.info(f"Space yaradildi: {repo_id}")
        except Exception as e:
            if "already exists" in str(e).lower():
                log.info(f"Space artiq movcuddur: {repo_id}")
            else:
                raise

        # 2. Dockerfile yukle
        dockerfile_content = USERBOT_DOCKERFILE.format(repo=GITHUB_REPO)
        with tempfile.NamedTemporaryFile(
            mode="w", suffix="Dockerfile", delete=False, encoding="utf-8"
        ) as f:
            f.write(dockerfile_content)
            temp_path = f.name

        try:
            api.upload_file(
                path_or_fileobj=temp_path,
                path_in_repo="Dockerfile",
                repo_id=repo_id,
                repo_type="space",
            )
        finally:
            os.unlink(temp_path)

        # 3. Secrets elave et
        secrets = {
            "API_KEY": str(context.user_data["api_id"]),
            "API_HASH": context.user_data["api_hash"],
            "STRING_SESSION": context.user_data["session"],
            "BOTLOG": "True",
            "BOTLOG_CHATID": str(context.user_data.get("botlog_chatid", 0)),
            "DATABASE_URL": "sqlite:///apex.db",
            "LANGUAGE": "DEFAULT",
            "PATTERNS": ".,",
            "HF_TOKEN": token,
            "HF_SPACE_ID": repo_id,
        }

        for key, value in secrets.items():
            api.add_space_secret(repo_id, key, value)

        log.info(f"Secrets elave edildi: {repo_id}")

        # 4. Ugurlu!
        text = (
            "<b>APEX Userbot Quruldu!</b>\n\n"
            f"Space: <a href='https://huggingface.co/spaces/{repo_id}'>{repo_id}</a>\n\n"
            "Bot <b>3-5 deqiqe</b> erzinde aktivlesecek.\n"
            "(Ilk defe Docker build oldugu ucun bir az uzun cekir)\n\n"
            "<b>Test etmek ucun:</b>\n"
            "Telegram-da her hansi sohbete <code>.alive</code> yazin\n\n"
            "<b>Esas emrler:</b>\n"
            "<code>.alive</code> - Bot aktiv oldugunu yoxla\n"
            "<code>.dbbackup</code> - Database backup\n"
            "<code>.update</code> - Botu yenile\n"
            "<code>.help</code> - Butun emrler\n\n"
            "Problem varsa: @apexsup"
        )
        await update.message.reply_text(
            text, parse_mode="HTML", disable_web_page_preview=True
        )

    except Exception as e:
        log.error(f"Space yaratma xetasi: {e}")
        await update.message.reply_text(
            f"Space yaradila bilmedi!\n\n"
            f"Xeta: <code>{e}</code>\n\n"
            "Yeniden cehd etmek ucun /setup yazin.",
            parse_mode="HTML",
        )

    context.user_data.clear()
    return ConversationHandler.END


# ==========================================
# /cancel
# ==========================================
async def cmd_cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await cleanup_client(context)
    context.user_data.clear()
    await update.message.reply_text(
        "Qurulum legv edildi.\nYeniden baslamaq ucun /setup yazin."
    )
    return ConversationHandler.END


# ==========================================
# Timeout handler
# ==========================================
async def timeout_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await cleanup_client(context)
    context.user_data.clear()
    if update and update.message:
        await update.message.reply_text(
            "Vaxt bitdi! Qurulum legv edildi.\nYeniden baslamaq ucun /setup yazin."
        )
    return ConversationHandler.END


# ==========================================
# MAIN
# ==========================================
def main():
    if not BOT_TOKEN:
        print("SETUP_BOT_TOKEN environment variable teyin edilmeyib!")
        print("@BotFather-den bot yaradib token-i SETUP_BOT_TOKEN olaraq teyin edin.")
        return

    # HuggingFace ucun health check server
    start_health_server()

    app = Application.builder().token(BOT_TOKEN).build()

    # Conversation handler
    conv = ConversationHandler(
        entry_points=[CommandHandler("setup", cmd_setup)],
        states={
            ASK_API_ID: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, step_api_id)
            ],
            ASK_API_HASH: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, step_api_hash)
            ],
            ASK_PHONE: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, step_phone)
            ],
            ASK_CODE: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, step_code)
            ],
            ASK_2FA: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, step_2fa)
            ],
            ASK_HF_TOKEN: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, step_hf_token)
            ],
            ConversationHandler.TIMEOUT: [
                MessageHandler(filters.ALL, timeout_handler)
            ],
        },
        fallbacks=[CommandHandler("cancel", cmd_cancel)],
        conversation_timeout=600,  # 10 deqiqe
        per_user=True,
        per_chat=True,
    )

    app.add_handler(CommandHandler("start", cmd_start))
    app.add_handler(conv)

    log.info("APEX Setup Bot isleyir...")

    # DNS fix — retry mexanizmi
    max_retries = 5
    for attempt in range(max_retries):
        try:
            # DNS yoxla
            subprocess.run(["nslookup", "api.telegram.org"], capture_output=True, timeout=5)
            log.info(f"DNS yoxlama ugurlu (cehd {attempt + 1})")
            app.run_polling(drop_pending_updates=True)
            break
        except Exception as e:
            log.warning(f"Cehd {attempt + 1}/{max_retries} ugursuz: {e}")
            if attempt < max_retries - 1:
                wait = 10 * (attempt + 1)
                log.info(f"{wait} saniye gozlenilir...")
                time.sleep(wait)
            else:
                log.error("Butun cehdler ugursuz oldu!")
                # Son cehd — birbaşa çalış
                app.run_polling(drop_pending_updates=True)


if __name__ == "__main__":
    main()
