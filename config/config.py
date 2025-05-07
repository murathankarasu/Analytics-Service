import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'uploads')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max dosya boyutu
    
    # Klasör yapısını oluştur
    @staticmethod
    def init_app(app):
        os.makedirs(os.path.join(Config.UPLOAD_FOLDER, 'images'), exist_ok=True)
        os.makedirs(os.path.join(Config.UPLOAD_FOLDER, 'videos'), exist_ok=True)
