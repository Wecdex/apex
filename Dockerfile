FROM python:3.9-slim

# Sistem asılılıqları
RUN apt-get update && apt-get install -y \
    git \
    ffmpeg \
    libcairo2-dev \
    && rm -rf /var/lib/apt/lists/*

# İş qovluğu
WORKDIR /app

# Requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Bütün faylları kopyala
COPY . .

# HuggingFace Spaces port 7860 gözləyir
EXPOSE 7860

# app.py ilə başlat (Flask + Bot)
CMD ["python3", "app.py"]
