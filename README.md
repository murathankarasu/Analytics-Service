# Analytics Service

Bu servis, metin, görsel ve video içeriklerini analiz ederek etiketler çıkaran bir API sunar.

## Özellikler

- Metin analizi ve anahtar kelime çıkarma
- Görsel analizi ve nesne tanıma
- Video analizi ve hareket tanıma

## Kurulum

1. Projeyi klonlayın:
```bash
git clone [repo-url]
cd Analytics-Service
```

2. Sanal ortam oluşturun ve aktifleştirin:
```bash
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# veya
.venv\Scripts\activate  # Windows
```

3. Bağımlılıkları yükleyin:
```bash
pip install -r requirements.txt
```

4. Uygulamayı çalıştırın:
```bash
python run.py
```

## API Kullanımı

### Metin Analizi
```http
POST /api/analyze/text
Content-Type: application/json

{
    "text": "Analiz edilecek metin"
}
```

### Görsel Analizi
```http
POST /api/analyze/image
Content-Type: multipart/form-data

file: [görsel dosyası]
```

### Video Analizi
```http
POST /api/analyze/video
Content-Type: multipart/form-data

file: [video dosyası]
```

## Deployment

Bu proje Railway üzerinde deploy edilebilir. Railway dashboard'undan yeni bir proje oluşturup GitHub reponuzu bağlayabilirsiniz.

## Lisans

MIT 