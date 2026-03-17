FROM python:3.11-slim

RUN apt-get update && apt-get install -y dnsutils curl && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 7860

CMD ["bash", "-c", "echo 'nameserver 8.8.8.8\nnameserver 1.1.1.1\nnameserver 8.8.4.4' > /etc/resolv.conf 2>/dev/null || true; python3 bot.py"]
