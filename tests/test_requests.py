import requests
import os

# Test dosyalarının yolları
TEST_IMAGE = "ba12d440bdca22e01aaeba8e5011147f.jpeg"
TEST_VIDEO = "v14044g50000cv9hg8vog65pe82rf2g0.mp4"
BASE_URL = "https://analytics-service-main-services.up.railway.app"

def test_text_analysis():
    """Metin analizi testi"""
    url = f"{BASE_URL}/analyze/text"
    test_texts = [
        "This is a beautiful day in New York City",
        "The movie was absolutely fantastic and I loved every minute of it",
        "The new iPhone features are amazing and innovative"
    ]
    
    for text in test_texts:
        response = requests.post(url, json={"text": text})
        print(f"\nMetin Analizi Sonucu:")
        print(f"Gönderilen metin: {text}")
        print(f"Durum kodu: {response.status_code}")
        print(f"Yanıt: {response.json()}")

def test_image_analysis():
    """Görsel analizi testi"""
    url = f"{BASE_URL}/analyze/image"
    
    # Test görselinin tam yolu
    image_path = os.path.join(os.path.dirname(__file__), TEST_IMAGE)
    
    with open(image_path, 'rb') as image_file:
        files = {'file': (TEST_IMAGE, image_file, 'image/webp')}
        response = requests.post(url, files=files)
        
        print(f"\nGörsel Analizi Sonucu:")
        print(f"Test dosyası: {TEST_IMAGE}")
        print(f"Durum kodu: {response.status_code}")
        print(f"Yanıt: {response.json()}")

def test_video_analysis():
    """Video analizi testi"""
    url = f"{BASE_URL}/analyze/video"
    
    # Test videosunun tam yolu
    video_path = os.path.join(os.path.dirname(__file__), TEST_VIDEO)
    
    with open(video_path, 'rb') as video_file:
        files = {'file': (TEST_VIDEO, video_file, 'video/mp4')}
        response = requests.post(url, files=files)
        
        print(f"\nVideo Analizi Sonucu:")
        print(f"Test dosyası: {TEST_VIDEO}")
        print(f"Durum kodu: {response.status_code}")
        print(f"Yanıt: {response.json()}")

if __name__ == "__main__":
    print("Analitik Servis Testleri Başlıyor...")
    print("=" * 50)
    
    try:
        test_text_analysis()
        test_image_analysis()
        test_video_analysis()
    except requests.exceptions.ConnectionError:
        print("\nHata: Sunucuya bağlanılamadı. Lütfen Flask uygulamasının çalıştığından emin olun.")
    except Exception as e:
        print(f"\nHata: {str(e)}")
    
    print("\nTestler tamamlandı.") 