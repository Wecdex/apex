"""
APEX Userbot — HuggingFace Spaces Launcher
Flask keepalive server + Bot başlatma
"""

import threading
import subprocess
import sys
import os

try:
    from dotenv import load_dotenv
    load_dotenv("config.env")
except ImportError:
    pass

from flask import Flask

app = Flask(__name__)

BOT_RUNNING = False

@app.route("/")
def home():
    status = "✅ Aktiv" if BOT_RUNNING else "⏳ Yüklənir..."
    
    # Konfiqurasiya yoxlanışı
    api_key = os.environ.get("API_KEY")
    string_session = os.environ.get("STRING_SESSION")
    botlog = os.environ.get("BOTLOG_CHATID")
    
    if not api_key or not string_session or not botlog:
        return f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>𝙰 𝙿 Σ 𝚇 — Quraşdırma</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ 
            background: linear-gradient(135deg, #0a0a1a 0%, #1a0a2e 50%, #0a1a2e 100%);
            color: #fff; font-family: 'Segoe UI', sans-serif; 
            min-height: 100vh; display: flex; align-items: center; justify-content: center;
        }}
        .container {{ 
            max-width: 600px; padding: 40px; 
            background: rgba(255,255,255,0.05); border-radius: 20px;
            border: 1px solid rgba(255,255,255,0.1);
            backdrop-filter: blur(10px);
        }}
        h1 {{ text-align: center; font-size: 2.5em; margin-bottom: 10px; }}
        .subtitle {{ text-align: center; color: #e94560; margin-bottom: 30px; }}
        .error {{ 
            background: rgba(233,69,96,0.2); border: 1px solid #e94560; 
            padding: 15px; border-radius: 10px; margin-bottom: 20px;
        }}
        .step {{ 
            background: rgba(255,255,255,0.05); padding: 15px; 
            border-radius: 10px; margin-bottom: 10px;
            border-left: 3px solid #e94560;
        }}
        .step-num {{ color: #e94560; font-weight: bold; }}
        a {{ color: #4ecdc4; }}
        code {{ background: rgba(255,255,255,0.1); padding: 2px 6px; border-radius: 4px; font-size: 0.9em; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>𝙰 𝙿 Σ 𝚇 ✨</h1>
        <p class="subtitle">Telegram Userbot</p>
        
        <div class="error">
            ⚠️ <strong>Konfiqurasiya tapılmadı!</strong> Aşağıdakı addımları izləyin:
        </div>
        
        <div class="step">
            <span class="step-num">1.</span> 
            <a href="https://my.telegram.org" target="_blank">my.telegram.org</a> saytından 
            <code>API ID</code> və <code>API Hash</code> alın
        </div>
        
        <div class="step">
            <span class="step-num">2.</span> 
            Telegram-da <a href="https://t.me/StringFatherBot" target="_blank">@StringFatherBot</a>-a yazıb 
            <code>String Session</code> alın
        </div>
        
        <div class="step">
            <span class="step-num">3.</span> 
            Bir Telegram qrupu yaradın, <a href="https://t.me/userinfobot" target="_blank">@userinfobot</a>-u 
            qrupa əlavə edib qrupun <code>ID</code>-sini öyrənin
        </div>
        
        <div class="step">
            <span class="step-num">4.</span> 
            Bu Space-in <strong>Settings → Variables and secrets</strong> bölməsinə girin və bu dəyərləri əlavə edin:<br><br>
            <code>API_KEY</code> = API ID rəqəmi<br>
            <code>API_HASH</code> = API Hash<br>
            <code>STRING_SESSION</code> = String Session kodu<br>
            <code>BOTLOG_CHATID</code> = Qrup ID-si<br>
            <code>BOTLOG</code> = True
        </div>
        
        <div class="step">
            <span class="step-num">5.</span> 
            Settings-dən <strong>"Factory reboot"</strong> basın. Bot başlayacaq! 🚀
        </div>
    </div>
</body>
</html>
"""
    
    return f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>𝙰 𝙿 Σ 𝚇 — Aktiv</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ 
            background: linear-gradient(135deg, #0a0a1a 0%, #1a0a2e 50%, #0a1a2e 100%);
            color: #fff; font-family: 'Segoe UI', sans-serif;
            min-height: 100vh; display: flex; align-items: center; justify-content: center;
        }}
        .container {{ 
            text-align: center; padding: 40px;
            background: rgba(255,255,255,0.05); border-radius: 20px;
            border: 1px solid rgba(255,255,255,0.1);
        }}
        h1 {{ font-size: 3em; margin-bottom: 10px; }}
        .status {{ 
            display: inline-block; padding: 8px 20px; border-radius: 20px;
            background: rgba(78,205,196,0.2); border: 1px solid #4ecdc4;
            color: #4ecdc4; font-size: 1.2em; margin-top: 15px;
        }}
        .info {{ color: #888; margin-top: 20px; font-size: 0.9em; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>𝙰 𝙿 Σ 𝚇 ✨</h1>
        <p style="color: #e94560; font-size: 1.2em;">Telegram Userbot</p>
        <div class="status">{status}</div>
        <p class="info">Bot işləyir. İstənilən söhbətə <code>.alive</code> yazıb test edin.</p>
    </div>
</body>
</html>
"""

@app.route("/health")
def health():
    return "OK", 200

def run_bot():
    """Botu ayrı prosesdə başlat — crash/restart olsa yenidən başlat."""
    import time
    global BOT_RUNNING

    while True:
        # Hər başlanğıcda GitHub-dan yenilikləri çək
        try:
            subprocess.run(
                ["git", "pull", "origin", "main"],
                capture_output=True, timeout=30
            )
        except Exception:
            pass

        BOT_RUNNING = True
        try:
            result = subprocess.run([sys.executable, "main.py"])
            exit_code = result.returncode
        except Exception:
            exit_code = 1

        BOT_RUNNING = False

        # Bot prosesi dayandı — yenidən başlat
        if exit_code == 0:
            # .restart və ya .update now — normal restart
            print(f"[app.py] Bot prosesi dayandı (kod: {exit_code}). 3 saniyə sonra yenidən başladılır...")
            time.sleep(3)
        else:
            # Crash — 5 saniyə gözlə, sonra restart
            print(f"[app.py] Bot prosesi crash etdi (kod: {exit_code}). 5 saniyə sonra yenidən başladılır...")
            time.sleep(5)


if __name__ == "__main__":
    # Konfiqurasiya varsa botu başlat
    if os.environ.get("API_KEY") and os.environ.get("STRING_SESSION"):
        bot_thread = threading.Thread(target=run_bot, daemon=True)
        bot_thread.start()

    # Flask server (port 7860 — HuggingFace gözləyir)
    app.run(host="0.0.0.0", port=7860)
