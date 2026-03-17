# Copyright (C) 2020
# U S Σ R Δ T O R 

""" UserBot hazırlanışı """

import os
import time
from re import compile
from sys import version_info
from logging import basicConfig, getLogger, INFO, DEBUG
def sb(val):
    """strtobool replacement (distutils removed in Python 3.13+)"""
    return str(val).lower() in ("1", "true", "yes", "on")
try:
    from pylast import LastFMNetwork, md5
except ImportError:
    LastFMNetwork = None
    md5 = lambda x: x
try:
    from pySmartDL import SmartDL
except ImportError:
    SmartDL = None
try:
    from dotenv import load_dotenv
except ImportError:
    load_dotenv = lambda *a, **kw: None
from requests import get
from telethon.tl.functions.channels import GetFullChannelRequest as getchat
from telethon.tl.functions.phone import GetGroupCallRequest as getvc
from telethon.tl.functions.channels import JoinChannelRequest
from telethon.sync import TelegramClient, custom
from telethon.sessions import StringSession
from telethon.events import callbackquery, InlineQuery, NewMessage
from math import ceil

load_dotenv("config.env")

StartTime = time.time()

# Bot log
CONSOLE_LOGGER_VERBOSE = sb(os.environ.get("CONSOLE_LOGGER_VERBOSE", "False"))

ASYNC_POOL = []

if CONSOLE_LOGGER_VERBOSE:
    basicConfig(
        format="%(asctime)s - @ApexOT - %(levelname)s - %(message)s",
        level=DEBUG,
    )
else:
    basicConfig(format="%(asctime)s - @ApexOT - %(levelname)s - %(message)s",
                level=INFO)
LOGS = getLogger(__name__)

if version_info[0] < 3 or version_info[1] < 6:
    LOGS.info("Ən az python 3.6 versiyasına sahib olmanız lazımdır."
              "Birdən çox özəllik buna bağlıdır. Bot söndürülür.")
    quit(1)

# APEX Userbot
# Config
CONFIG_CHECK = os.environ.get(
    "___________XAİŞ_______BU_____SETİRİ_____SILIN__________", None)

if CONFIG_CHECK:
    LOGS.info(
        "Xaiş ilk haştağ'da seçilən sətiri config.env faylından silin."
    )
    quit(1)

# Bot'un dili
LANGUAGE = os.environ.get("LANGUAGE", "DEFAULT").upper()

if not LANGUAGE in ["EN", "TR", "AZ", "UZ", "DEFAULT"]:
    LOGS.info("Bilinməyən bir dil seçdiniz. Buna görə DEFAULT işlədilir.")
    LANGUAGE = "DEFAULT"
    
# APEX Versiyası
APEX_VERSION = "3.1"

# Telegram API KEY ve HASH
_api_key_raw = os.environ.get("API_KEY", None)
try:
    API_KEY = int(_api_key_raw) if _api_key_raw else None
except (ValueError, TypeError):
    API_KEY = None
API_HASH = os.environ.get("API_HASH", None)

try:
    _sudo_raw = os.environ.get("SUDO_ID", "").strip()
    SUDO_ID = set(int(x) for x in _sudo_raw.split() if x.strip())
except (ValueError, TypeError):
    SUDO_ID = set()

SILINEN_PLUGIN = {}
# UserBot Session String
STRING_SESSION = os.environ.get("STRING_SESSION", None)

# Kanal / Qrup ID
_botlog_raw = os.environ.get("BOTLOG_CHATID", None)
try:
    BOTLOG_CHATID = int(_botlog_raw) if _botlog_raw else 0
except (ValueError, TypeError):
    BOTLOG_CHATID = 0

# Günlük
BOTLOG = sb(os.environ.get("BOTLOG", "False"))
LOGSPAMMER = sb(os.environ.get("LOGSPAMMER", "False"))

# PM
PM_AUTO_BAN = sb(os.environ.get("PM_AUTO_BAN", "False"))



# Yenilənmə
UPSTREAM_REPO_URL = os.environ.get(
    "UPSTREAM_REPO_URL",
    "https://github.com/Wecdex/apex.git")

# Konsol
CONSOLE_LOGGER_VERBOSE = sb(os.environ.get("CONSOLE_LOGGER_VERBOSE", "False"))

# SQL
DB_URI = os.environ.get("DATABASE_URL", "sqlite:///apex.db")

# OCR API key
OCR_SPACE_API_KEY = os.environ.get("OCR_SPACE_API_KEY", None)

# remove.bg API key
REM_BG_API_KEY = os.environ.get("REM_BG_API_KEY", None)

# AUTO PP
AUTO_PP = os.environ.get("AUTO_PP", None)

# Alive Name
ALIVE_NAME = os.environ.get("ALIVE_NAME", None)

# Warn modül
WARN_LIMIT = int(os.environ.get("WARN_LIMIT", 3))
WARN_MODE = os.environ.get("WARN_MODE", "gmute")

if not WARN_MODE in ["gmute", "gban"]:
    WARN_MODE = "gmute"

# Qaleriya
GALERI_SURE = int(os.environ.get("GALERI_SURE", 60))

# Chrome
CHROME_DRIVER = os.environ.get("CHROME_DRIVER", None)
GOOGLE_CHROME_BIN = os.environ.get("GOOGLE_CHROME_BIN", None)

PLUGINID = os.environ.get("PLUGIN_CHANNEL_ID", None)
# Plugin İçin
if not PLUGINID:
    PLUGIN_CHANNEL_ID = "me"
else:
    PLUGIN_CHANNEL_ID = int(PLUGINID)

# OpenWeatherMap API Key
OPEN_WEATHER_MAP_APPID = os.environ.get("OPEN_WEATHER_MAP_APPID", None)
WEATHER_DEFCITY = os.environ.get("WEATHER_DEFCITY", None)

# Lydia API
LYDIA_API_KEY = os.environ.get("LYDIA_API_KEY", None)

# Alive şəkil
IMG = os.environ.get(
    "IMG",
    "https://telegra.ph/file/2d7769a2ee6ae14e567d6.jpg")

# Anti Spambot
ANTI_SPAMBOT = sb(os.environ.get("ANTI_SPAMBOT", "False"))
ANTI_SPAMBOT_SHOUT = sb(os.environ.get("ANTI_SPAMBOT_SHOUT", "False"))

# Youtube API key
YOUTUBE_API_KEY = os.environ.get("YOUTUBE_API_KEY", None)

# Saat & Tarix
COUNTRY = str(os.environ.get("COUNTRY", ""))
TZ_NUMBER = int(os.environ.get("TZ_NUMBER", 1))

# Qarşılama
CLEAN_WELCOME = sb(os.environ.get("CLEAN_WELCOME", "True"))

# Last.fm
BIO_PREFIX = os.environ.get("BIO_PREFIX", "@apexsup | ")
DEFAULT_BIO = os.environ.get("DEFAULT_BIO", None)

LASTFM_API = os.environ.get("LASTFM_API", None)
LASTFM_SECRET = os.environ.get("LASTFM_SECRET", None)
LASTFM_USERNAME = os.environ.get("LASTFM_USERNAME", None)
LASTFM_PASSWORD_PLAIN = os.environ.get("LASTFM_PASSWORD", None)
try:
    LASTFM_PASS = md5(LASTFM_PASSWORD_PLAIN) if LASTFM_PASSWORD_PLAIN else None
except Exception:
    LASTFM_PASS = None
if LastFMNetwork and LASTFM_API and LASTFM_SECRET and LASTFM_USERNAME and LASTFM_PASS:
    try:
        lastfm = LastFMNetwork(api_key=LASTFM_API,
                               api_secret=LASTFM_SECRET,
                               username=LASTFM_USERNAME,
                               password_hash=LASTFM_PASS)
    except Exception:
        lastfm = None
else:
    lastfm = None

# Google Drive
G_DRIVE_CLIENT_ID = os.environ.get("G_DRIVE_CLIENT_ID", None)
G_DRIVE_CLIENT_SECRET = os.environ.get("G_DRIVE_CLIENT_SECRET", None)
G_DRIVE_AUTH_TOKEN_DATA = os.environ.get("G_DRIVE_AUTH_TOKEN_DATA", None)
GDRIVE_FOLDER_ID = os.environ.get("GDRIVE_FOLDER_ID", None)
TEMP_DOWNLOAD_DIRECTORY = os.environ.get("TMP_DOWNLOAD_DIRECTORY",
                                         "./downloads")
DEFAULT_NAME = os.environ.get("DEFAULT_NAME", None)
# Inline bot
BOT_TOKEN = os.environ.get("BOT_TOKEN", None)
BOT_USERNAME = os.environ.get("BOT_USERNAME", None)

# Genius
GENIUS = os.environ.get("GENIUS", None)
CMD_HELP = {}
CMD_HELP_BOT = {}
PM_AUTO_BAN_LIMIT = int(os.environ.get("PM_AUTO_BAN_LIMIT", 4))

SPOTIFY_DC = os.environ.get("SPOTIFY_DC", None)
SPOTIFY_KEY = os.environ.get("SPOTIFY_KEY", None)

PAKET_ISMI = os.environ.get("PAKET_ISMI", "@apexsup Paketi")

# Avto
AVTO_Q = sb(os.environ.get("AVTO_Q", "True"))

# Pattern
PATTERNS = os.environ.get("PATTERNS", ".,")
WHITELIST = [1419590194, 5105666086, 723397979]

# Təhlükəli pluginlər üçün
TEHLUKELI = ["SESSION", "API_HASH", "API_KEY", r"\.session\.save", "EditBannedRequest", "ChatBannedRights", "kick_participiant", "UploadProfilePhotoRequest", "ChatAdminRights", "EditAdminRequest", r"\.revert", r"\.klon", r"\.UpdateProfileRequest"]

# CloudMail.ru və MEGA.nz
if not os.path.exists('bin'):
    os.mkdir('bin')

binaries = {
    "https://raw.githubusercontent.com/yshalsager/megadown/master/megadown":
    "bin/megadown",
    "https://raw.githubusercontent.com/yshalsager/cmrudl.py/master/cmrudl.py":
    "bin/cmrudl"
}

for binary, path in binaries.items():
    try:
        if SmartDL and not os.path.exists(path):
            downloader = SmartDL(binary, path, progress_bar=False)
            downloader.start()
            if os.name != 'nt':  # Windows-da chmod lazım deyil
                os.chmod(path, 0o755)
    except Exception as e:
        LOGS.warning(f"Binary yüklənə bilmədi: {path} — {e}")

# 'bot' dəyişkəni
# Python 3.14+ event loop fix
import asyncio
try:
    asyncio.get_running_loop()
except RuntimeError:
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

# Session Manager — STRING_SESSION boşdursa avtomatik yarat
if not STRING_SESSION or not STRING_SESSION.strip():
    LOGS.info("STRING_SESSION tapılmadı. Yeni session yaradılır...")
    from userbot.session_manager import get_or_create_session
    STRING_SESSION = get_or_create_session(API_KEY, API_HASH, STRING_SESSION)
    
    # Session yaradıldıqdan sonra botu yenidən başlatmaq lazımdır
    LOGS.info("Session yaradıldı. Botu yenidən başlatın: python app.py")
    import sys
    sys.exit(0)

if STRING_SESSION:
    # pylint: devre dışı=geçersiz ad
    bot = TelegramClient(StringSession(STRING_SESSION), API_KEY, API_HASH)
else:
    # pylint: devre dışı=geçersiz ad
    bot = TelegramClient("userbot", API_KEY, API_HASH)



async def get_call(event):
    mm = await event.client(getchat(event.chat_id))
    xx = await event.client(getvc(mm.full_chat.call))
    return xx.call

async def check_botlog_chatid():
    global BOTLOG, LOGSPAMMER
    if not BOTLOG_CHATID and LOGSPAMMER:
        LOGS.info(
            "⚠️ BOTLOG_CHATID təyin edilməyib. LOGSPAMMER deaktiv edilir.")
        LOGSPAMMER = False

    if not BOTLOG_CHATID and BOTLOG:
        LOGS.info(
            "⚠️ BOTLOG_CHATID təyin edilməyib. BOTLOG deaktiv edilir. "
            "Aktivləşdirmək üçün BOTLOG_CHATID-i düzgün qrup ID ilə təyin edin.")
        BOTLOG = False
        return

    if not BOTLOG and not LOGSPAMMER:
        return

    try:
        entity = await bot.get_entity(BOTLOG_CHATID)
        if entity.default_banned_rights.send_messages:
            LOGS.info(
                "⚠️ BOTLOG_CHATID qrupuna mesaj göndərmə icazəsi yoxdur. "
                "BOTLOG deaktiv edilir. Qrup ID-ni yoxlayın.")
            BOTLOG = False
    except Exception as e:
        LOGS.info(
            f"⚠️ BOTLOG_CHATID ({BOTLOG_CHATID}) etibarsızdır: {e}. "
            "BOTLOG deaktiv edilir.")
        BOTLOG = False
        
if BOT_TOKEN and BOT_TOKEN.strip():
    try:
        tgbot = TelegramClient(
            "TG_BOT_TOKEN",
            api_id=API_KEY,
            api_hash=API_HASH
        ).start(bot_token=BOT_TOKEN)
        LOGS.info("Inline bot aktivləşdirildi.")
    except Exception as e:
        LOGS.warning(f"Inline bot başladıla bilmədi: {e}")
        tgbot = None
else:
    tgbot = None
    LOGS.info("BOT_TOKEN yoxdur, inline bot deaktivdir.")

def butonlastir(sayfa, moduller):
    Satir = 5
    Kolon = 2
    
    moduller = sorted([modul for modul in moduller if not modul.startswith("_")])
    pairs = list(map(list, zip(moduller[::2], moduller[1::2])))
    if len(moduller) % 2 == 1:
        pairs.append([moduller[-1]])
    max_pages = ceil(len(pairs) / Satir)
    pairs = [pairs[i:i + Satir] for i in range(0, len(pairs), Satir)]
    butonlar = []
    for pairs in pairs[sayfa]:
        butonlar.append([
            custom.Button.inline("🔸 " + pair, data=f"bilgi[{sayfa}]({pair})") for pair in pairs
        ])

    butonlar.append([custom.Button.inline("◀️ Geri", data=f"sayfa({(max_pages - 1) if sayfa == 0 else (sayfa - 1)})"), custom.Button.inline("İrəli ▶️", data=f"sayfa({0 if sayfa == (max_pages - 1) else sayfa + 1})")])
    return [max_pages, butonlar]


with bot:
    if AVTO_Q:
        try:
            bot(JoinChannelRequest("@apexsup"))
            bot(JoinChannelRequest("@apexuserbot"))
        except:
            pass

    moduller = CMD_HELP
    me = bot.get_me()
    uid = me.id

    try:
        @tgbot.on(NewMessage(pattern='/start'))
        async def start_bot_handler(event):
            if not event.message.from_id == uid:
                await event.reply(f'`Salam mən ` @apexuserbot`! Mən sahibimə (`@{me.username}`) kömək olmaq üçün varam, yəni sənə köməkçi ola bilmərəm :/ Ama sən də bir APEX Userbot quraşdıra bilərsən; Kanala bax` @apexuserbot')
            else:
                await event.reply(f'`𝙰 𝙿 Σ 𝚇`')

        @tgbot.on(InlineQuery)  # pylint:disable=E0602
        async def inline_handler(event):
            builder = event.builder
            result = None
            query = event.text
            if event.query.user_id == uid and query == "@ApexOT":
                rev_text = query[::-1]
                veriler = (butonlastir(0, sorted(CMD_HELP)))
                result = await builder.article(
                    f"Xaiş sadəcə .kömek əmri ilə işladin",
                    text=f"**𝙰 𝙿 Σ 𝚇** [𝙰 𝙿 Σ 𝚇](https://t.me/apexuserbot) __⚡__\n\n**Yüklənən Modul Sayı:** `{len(CMD_HELP)}`\n**Səhifə:** 1/{veriler[0]}",
                    buttons=veriler[1],
                    link_preview=False
                )
            elif query.startswith("http"):
                parca = query.split(" ")
                result = builder.article(
                    "Fayl Yükləndi",
                    text=f"**Fayl uğurlu bir şəkildə {parca[2]} saytına yükləndi!**\n\nYükləmə zamanı: {parca[1][:3]} saniyə\n[‏‏‎ ‎]({parca[0]})",
                    buttons=[
                        [custom.Button.url('URL', parca[0])]
                    ],
                    link_preview=True
                )
            else:
                result = builder.article(
                    "@apexuserbot",
                    text="""@apexuserbot'u işlətməyi yoxlayın!
Hesabınızı bot'a çevirə bilərsiz və bunları işlədə bilərsiz. Unutmayın, siz başqasının botunu idarə edə bilmərsiz! Altdakı GitHub adresindən bütün qurulum haqda məlumat var.""",
                    buttons=[
                        [custom.Button.url("Kanala Qatıl", "https://t.me/apexuserbot"), custom.Button.url(
                            "Qrupa Qatıl", "https://t.me/apexsup")],
                        [custom.Button.url(
                            "GitHub", "https://github.com/sahibziko/delta")]
                    ],
                    link_preview=False
                )
            await event.answer([result] if result else None)

        @tgbot.on(callbackquery.CallbackQuery(data=compile(rb"sayfa\((.+?)\)")))
        async def sayfa(event):
            if not event.query.user_id == uid: 
                return await event.answer("❌ Hey! Mənim mesajlarımı düzəltməyə çalışma! Özünə bir @apexuserbot qur.", cache_time=0, alert=True)
            sayfa = int(event.data_match.group(1).decode("UTF-8"))
            veriler = butonlastir(sayfa, CMD_HELP)
            await event.edit(
                f"**𝙰 𝙿 Σ 𝚇** [ApexOT](https://t.me/ApexOT) __işləyir__\n\n**Yüklənən Modul Sayı:** `{len(CMD_HELP)}`\n**Səhifə:** {sayfa + 1}/{veriler[0]}",
                buttons=veriler[1],
                link_preview=False
            )
        
        @tgbot.on(callbackquery.CallbackQuery(data=compile(rb"bilgi\[(\d*)\]\((.*)\)")))
        async def bilgi(event):
            if not event.query.user_id == uid: 
                return await event.answer("❌  Hey! Mənim mesajlarımı düzəltməyə çalışma! Özünə bir @apexuserbot qur.", cache_time=0, alert=True)

            sayfa = int(event.data_match.group(1).decode("UTF-8"))
            komut = event.data_match.group(2).decode("UTF-8")
            try:
                butonlar = [custom.Button.inline("🔹 " + cmd[0], data=f"komut[{komut}[{sayfa}]]({cmd[0]})") for cmd in CMD_HELP_BOT[komut]['commands'].items()]
            except KeyError:
                return await event.answer("❌ Bu modula açıqlama yazılmayıb.", cache_time=0, alert=True)

            butonlar = [butonlar[i:i + 2] for i in range(0, len(butonlar), 2)]
            butonlar.append([custom.Button.inline("◀️ Geri", data=f"sayfa({sayfa})")])
            await event.edit(
                f"**📗 Fayl:** `{komut}`\n**🔢 Əmr sayı:** `{len(CMD_HELP_BOT[komut]['commands'])}`",
                buttons=butonlar,
                link_preview=False
            )
        
        @tgbot.on(callbackquery.CallbackQuery(data=compile(rb"komut\[(.*)\[(\d*)\]\]\((.*)\)")))
        async def komut(event):
            if not event.query.user_id == uid: 
                return await event.answer("❌ Hey! Mənim mesajlarımı düzəltməyə çalışma! Özünə bir @apexuserbot qur.", cache_time=0, alert=True)

            cmd = event.data_match.group(1).decode("UTF-8")
            sayfa = int(event.data_match.group(2).decode("UTF-8"))
            komut = event.data_match.group(3).decode("UTF-8")

            result = f"**📗 Fayl:** `{cmd}`\n"
            if CMD_HELP_BOT[cmd]['info']['info'] == '':
                if not CMD_HELP_BOT[cmd]['info']['warning'] == '':
                    result += f"**⬇️ Rəsmi:** {'✅' if CMD_HELP_BOT[cmd]['info']['official'] else '❌'}\n"
                    result += f"**⚠️ Xəbərdarlıq:** {CMD_HELP_BOT[cmd]['info']['warning']}\n\n"
                else:
                    result += f"**⬇️ Rəsmi:** {'✅' if CMD_HELP_BOT[cmd]['info']['official'] else '❌'}\n\n"
            else:
                result += f"**⬇️ Rəsmi:** {'✅' if CMD_HELP_BOT[cmd]['info']['official'] else '❌'}\n"
                if not CMD_HELP_BOT[cmd]['info']['warning'] == '':
                    result += f"**⚠️ Xəbərdarlıq:** {CMD_HELP_BOT[cmd]['info']['warning']}\n"
                result += f"**ℹ️ Info:** {CMD_HELP_BOT[cmd]['info']['info']}\n\n"

            command = CMD_HELP_BOT[cmd]['commands'][komut]
            if command['params'] is None:
                result += f"**🛠 Əmr:** `{PATTERNS[:1]}{command['command']}`\n"
            else:
                result += f"**🛠 Əmr:** `{PATTERNS[:1]}{command['command']} {command['params']}`\n"
                
            if command['example'] is None:
                result += f"**💬 Açıqlama:** `{command['usage']}`\n\n"
            else:
                result += f"**💬 Açıqlama:** `{command['usage']}`\n"
                result += f"**⌨️ Məsələn:** `{PATTERNS[:1]}{command['example']}`\n\n"

            await event.edit(
                result,
                buttons=[custom.Button.inline("◀️ Geri", data=f"bilgi[{sayfa}]({cmd})")],
                link_preview=False
            )
    except Exception as e:
        print(e)
        LOGS.info(
            "Botunuzda inline dəstəyi deaktiv edildi. "
            "Aktivləşdirmək üçün bir bot token tanımlayın və botunuzda inline modunu aktivləşdirin. "
            "Əgər bunun xaricində bir problem olduğunu düşünürsüzsə bizlə əlaqə saxlayın."
        )

    try:
        bot.loop.run_until_complete(check_botlog_chatid())
    except Exception as e:
        LOGS.info(
            f"⚠️ BOTLOG yoxlanışı zamanı xəta: {e}. "
            "BOTLOG deaktiv edilir."
        )
        BOTLOG = False


# Qlobal dəyişkənlər
SON_GORULME = 0
COUNT_MSG = 0
USERS = {}
BRAIN_CHECKER = []
COUNT_PM = {}
LASTMSG = {}
ENABLE_KILLME = True
ISAFK = False
AFKREASON = None
ZALG_LIST = [[
    "̖",
    " ̗",
    " ̘",
    " ̙",
    " ̜",
    " ̝",
    " ̞",
    " ̟",
    " ̠",
    " ̤",
    " ̥",
    " ̦",
    " ̩",
    " ̪",
    " ̫",
    " ̬",
    " ̭",
    " ̮",
    " ̯",
    " ̰",
    " ̱",
    " ̲",
    " ̳",
    " ̹",
    " ̺",
    " ̻",
    " ̼",
    " ͅ",
    " ͇",
    " ͈",
    " ͉",
    " ͍",
    " ͎",
    " ͓",
    " ͔",
    " ͕",
    " ͖",
    " ͙",
    " ͚",
    " ",
],
    [
    " ̍", " ̎", " ̄", " ̅", " ̿", " ̑", " ̆", " ̐", " ͒", " ͗",
    " ͑", " ̇", " ̈", " ̊", " ͂", " ̓", " ̈́", " ͊", " ͋", " ͌",
    " ̃", " ̂", " ̌", " ͐", " ́", " ̋", " ̏", " ̽", " ̉", " ͣ",
    " ͤ", " ͥ", " ͦ", " ͧ", " ͨ", " ͩ", " ͪ", " ͫ", " ͬ", " ͭ",
    " ͮ", " ͯ", " ̾", " ͛", " ͆", " ̚"
],
    [
    " ̕",
    " ̛",
    " ̀",
    " ́",
    " ͘",
    " ̡",
    " ̢",
    " ̧",
    " ̨",
    " ̴",
    " ̵",
    " ̶",
    " ͜",
    " ͝",
    " ͞",
    " ͟",
    " ͠",
    " ͢",
    " ̸",
    " ̷",
    " ͡",
]]
