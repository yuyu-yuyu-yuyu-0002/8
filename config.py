import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Firebase 配置
    FIREBASE_CREDENTIALS = os.environ.get("FIREBASE_CREDENTIALS")
    
    # 檔案上傳配置
    MAX_FILE_SIZE = int(os.environ.get("MAX_FILE_SIZE", 10485760))  # 10MB
    ALLOWED_EXTENSIONS = os.environ.get("ALLOWED_EXTENSIONS", "pdf,doc,docx,txt,md").split(',')
    
    # Flask 配置
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-key")
    
    # 環境設定
    FLASK_ENV = os.environ.get("FLASK_ENV", "development")
    
    @staticmethod
    def is_allowed_file(filename):
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in Config.ALLOWED_EXTENSIONS