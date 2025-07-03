from flask import Flask
from flask_cors import CORS
from config import Config
from routes.knowledge_routes import knowledge_bp
from routes.upload_routes import upload_bp
from routes.statistics_routes import statistics_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # 啟用 CORS
    CORS(app, origins=[
    "https://line-knowledge.vercel.app",
    "http://localhost:3000",  # 本地開發用
    "http://localhost:8080"   # 本地開發用
])
    
    # 註冊藍圖
    app.register_blueprint(knowledge_bp, url_prefix='/api')
    app.register_blueprint(upload_bp, url_prefix='/api')
    app.register_blueprint(statistics_bp, url_prefix='/api')
    
    # 健康檢查端點
    @app.route('/health')
    def health_check():
        return {"status": "healthy", "message": "LINE AI BOT API is running"}
    
    return app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
