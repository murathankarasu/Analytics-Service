from flask import Flask
from config.config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    from app.routes import main
    app.register_blueprint(main.bp)
    
    return app

app = create_app()
