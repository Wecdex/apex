@echo off
REM ============================================
REM 𝙰 𝙿 Σ 𝚇 Userbot - CMD Run Skripti
REM ============================================
REM İstifadə: run.bat

chcp 65001 >nul
color 0B

echo ============================================
echo   𝙰 𝙿 Σ 𝚇 Userbot - Lokal İşə Salma
echo ============================================
echo.

REM config.env faylını yoxla
if not exist "config.env" (
    echo [XƏTA] config.env faylı tapılmadı!
    echo.
    echo Həll yolu:
    echo 1. config.env.example faylını kopyalayın
    echo 2. Adını 'config.env' edin
    echo 3. İçindəki dəyərləri doldurun
    echo.
    echo Əmr: copy config.env.example config.env
    echo.
    pause
    exit /b 1
)

echo [✓] config.env tapıldı

REM config.env-dən environment dəyişənlərini yüklə
echo [→] Environment dəyişənləri yüklənir...

for /f "usebackq tokens=1,* delims==" %%a in ("config.env") do (
    set "line=%%a"
    if not "!line:~0,1!"=="#" (
        if not "%%a"=="" (
            set "%%a=%%b"
        )
    )
)

setlocal enabledelayedexpansion

echo [✓] Environment dəyişənləri yükləndi

REM Python yoxla
echo [→] Python yoxlanılır...
python --version >nul 2>&1
if errorlevel 1 (
    echo [XƏTA] Python tapılmadı!
    echo Python 3.9+ quraşdırın: https://www.python.org/downloads/
    pause
    exit /b 1
)

for /f "tokens=*" %%i in ('python --version') do set PYTHON_VER=%%i
echo [✓] %PYTHON_VER% tapıldı

REM Virtual environment yoxla
if not exist ".venv" (
    echo [!] Virtual environment tapılmadı. Yaradılır...
    python -m venv .venv
    echo [✓] Virtual environment yaradıldı
)

REM Virtual environment aktivləşdir
echo [→] Virtual environment aktivləşdirilir...
call .venv\Scripts\activate.bat
echo [✓] Virtual environment aktiv

REM Requirements yoxla və quraşdır
echo [→] Asılılıqlar yoxlanılır...
if exist "requirements.txt" (
    echo [→] pip paketləri quraşdırılır (bu bir neçə dəqiqə çəkə bilər)...
    pip install --quiet --upgrade pip
    pip install --quiet -r requirements.txt
    echo [✓] Bütün asılılıqlar quraşdırıldı
) else (
    echo [XƏBƏRDARLIQ] requirements.txt tapılmadı
)

echo.
echo ============================================
echo   Bot başladılır...
echo ============================================
echo.
echo Flask server: http://localhost:7860
echo Health check: http://localhost:7860/health
echo.
echo Dayandırmaq üçün: Ctrl+C
echo.

REM Botu başlat
python app.py
