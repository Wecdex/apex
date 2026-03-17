#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
APEX Userbot - Session Manager
Avtomatik string session yaradır və config.env-ə yazır
"""
import os
from telethon.sync import TelegramClient
from telethon.sessions import StringSession

def update_config_env(key, value):
    """config.env faylında key=value yenilə və ya əlavə et"""
    config_path = "config.env"
    
    if not os.path.exists(config_path):
        # config.env yoxdursa, config.env.example-dan kopyala
        if os.path.exists("config.env.example"):
            with open("config.env.example", "r", encoding="utf-8") as f:
                content = f.read()
            with open(config_path, "w", encoding="utf-8") as f:
                f.write(content)
        else:
            # Heç biri yoxdursa, boş fayl yarat
            with open(config_path, "w", encoding="utf-8") as f:
                f.write("")
    
    # config.env-i oxu
    with open(config_path, "r", encoding="utf-8") as f:
        lines = f.readlines()
    
    # Key-i tap və yenilə
    found = False
    new_lines = []
    
    for line in lines:
        if line.strip().startswith(f"{key}="):
            new_lines.append(f"{key}={value}\n")
            found = True
        else:
            new_lines.append(line)
    
    # Tapılmadısa, əlavə et
    if not found:
        new_lines.append(f"\n# Avtomatik yaradılmış string session\n{key}={value}\n")
    
    # Yaz
    with open(config_path, "w", encoding="utf-8") as f:
        f.writelines(new_lines)
    
    print(f"✓ config.env yeniləndi: {key}")

def create_session(api_id, api_hash):
    """Yeni string session yarat"""
    print("\n" + "=" * 60)
    print("APEX Userbot - İlk Quraşdırma")
    print("=" * 60)
    print("\nTelegram hesabınıza giriş etmək üçün məlumatlar lazımdır.")
    print("Telefon nömrənizi beynəlxalq formatda yazın (məs: +994501234567)\n")
    
    # StringSession ilə client yarat
    with TelegramClient(StringSession(), api_id, api_hash) as client:
        # start() telefon nömrəsi soruşacaq və giriş edəcək
        print("\n✓ Telegram-a uğurla giriş edildi!")
        
        # String session-u götür
        session_string = client.session.save()
        
        # config.env-ə yaz
        update_config_env("STRING_SESSION", session_string)
        
        print("\n" + "=" * 60)
        print("✓ String session avtomatik olaraq config.env-ə yazıldı!")
        print("=" * 60)
        print("\nİndi botu yenidən başlatın: python app.py")
        print("Növbəti başlanğıclarda avtomatik giriş edəcək.\n")
        
        return session_string

def get_or_create_session(api_id, api_hash, current_session=None):
    """Mövcud session-u yoxla, yoxdursa yarat"""
    if current_session and current_session.strip():
        # Session var, istifadə et
        return current_session
    else:
        # Session yoxdur, yarat
        return create_session(api_id, api_hash)
