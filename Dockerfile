# Python 3.11 base image kullan
FROM python:3.11-slim

# Çalışma dizinini ayarla
WORKDIR /app

# Sistem bağımlılıklarını yükle
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Gerekli dosyaları kopyala
COPY requirements.txt .
COPY . .

# Python bağımlılıklarını yükle
RUN pip install --no-cache-dir -r requirements.txt

# Uploads klasörünü oluştur
RUN mkdir -p uploads/images uploads/videos

# Port ayarı
EXPOSE 8000

# Uygulamayı çalıştır
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "app:app"] 