FROM python:3.11-slim

# Sistem asılılıqları
RUN apt-get update && apt-get install -y \
    git \
    neofetch \
    ffmpeg \
    libcairo2-dev \
    && rm -rf /var/lib/apt/lists/*

# İş qovluğu
WORKDIR /app

# Bütün faylları kopyala
COPY . .

# Requirements
RUN pip install --no-cache-dir -r requirements.txt || true

# HuggingFace Spaces port 7860 gözləyir
EXPOSE 7860

# Startup: git pull (yeniləmə), sonra app.py
CMD ["bash", "-c", "git pull origin main 2>/dev/null || true; python3 app.py"]
