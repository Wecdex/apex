# ============================================
# 𝙰 𝙿 Σ 𝚇 Userbot - PowerShell Run Skripti
# ============================================
# İstifadə: .\run.ps1

Write-Host "============================================" -ForegroundColor Cyan
Write-Host "  𝙰 𝙿 Σ 𝚇 Userbot - Lokal İşə Salma" -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""

# config.env faylını yoxla
if (-Not (Test-Path "config.env")) {
    Write-Host "[XƏTA] config.env faylı tapılmadı!" -ForegroundColor Red
    Write-Host ""
    Write-Host "Həll yolu:" -ForegroundColor Yellow
    Write-Host "1. config.env.example faylını kopyalayın" -ForegroundColor White
    Write-Host "2. Adını 'config.env' edin" -ForegroundColor White
    Write-Host "3. İçindəki dəyərləri doldurun (API_KEY, STRING_SESSION və s.)" -ForegroundColor White
    Write-Host ""
    Write-Host "Əmr: Copy-Item config.env.example config.env" -ForegroundColor Green
    Write-Host ""
    exit 1
}

Write-Host "[✓] config.env tapıldı" -ForegroundColor Green

# config.env-dən environment dəyişənlərini yüklə
Write-Host "[→] Environment dəyişənləri yüklənir..." -ForegroundColor Yellow

Get-Content "config.env" | ForEach-Object {
    $line = $_.Trim()
    # Boş sətir və şərh sətirləri keç
    if ($line -and -not $line.StartsWith("#")) {
        $parts = $line -split "=", 2
        if ($parts.Length -eq 2) {
            $key = $parts[0].Trim()
            $value = $parts[1].Trim()
            [System.Environment]::SetEnvironmentVariable($key, $value, "Process")
        }
    }
}

Write-Host "[✓] Environment dəyişənləri yükləndi" -ForegroundColor Green

# Python yoxla
Write-Host "[→] Python yoxlanılır..." -ForegroundColor Yellow
$pythonCmd = Get-Command python -ErrorAction SilentlyContinue

if (-Not $pythonCmd) {
    Write-Host "[XƏTA] Python tapılmadı!" -ForegroundColor Red
    Write-Host "Python 3.9+ quraşdırın: https://www.python.org/downloads/" -ForegroundColor Yellow
    exit 1
}

$pythonVersion = python --version
Write-Host "[✓] $pythonVersion tapıldı" -ForegroundColor Green

# Virtual environment yoxla
if (-Not (Test-Path ".venv")) {
    Write-Host "[!] Virtual environment tapılmadı. Yaradılır..." -ForegroundColor Yellow
    python -m venv .venv
    Write-Host "[✓] Virtual environment yaradıldı" -ForegroundColor Green
}

# Virtual environment aktivləşdir
Write-Host "[→] Virtual environment aktivləşdirilir..." -ForegroundColor Yellow
& ".venv\Scripts\Activate.ps1"
Write-Host "[✓] Virtual environment aktiv" -ForegroundColor Green

# Requirements yoxla və quraşdır
Write-Host "[→] Asılılıqlar yoxlanılır..." -ForegroundColor Yellow
if (Test-Path "requirements.txt") {
    Write-Host "[→] pip paketləri quraşdırılır (bu bir neçə dəqiqə çəkə bilər)..." -ForegroundColor Yellow
    pip install --quiet --upgrade pip
    pip install --quiet -r requirements.txt
    Write-Host "[✓] Bütün asılılıqlar quraşdırıldı" -ForegroundColor Green
} else {
    Write-Host "[XƏBƏRDARLIQ] requirements.txt tapılmadı" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "============================================" -ForegroundColor Cyan
Write-Host "  Bot başladılır..." -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Flask server: http://localhost:7860" -ForegroundColor Green
Write-Host "Health check: http://localhost:7860/health" -ForegroundColor Green
Write-Host ""
Write-Host "Dayandırmaq üçün: Ctrl+C" -ForegroundColor Yellow
Write-Host ""

# Botu başlat
python app.py
