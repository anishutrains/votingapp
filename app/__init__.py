from flask import Flask
from config import Config
import os

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Set a secret key for session management
    app.secret_key = os.environ.get('SECRET_KEY', 'dev-key-for-voting-app')
    
    # Configure session to be permanent
    app.config['PERMANENT_SESSION_LIFETIME'] = 3600  # 1 hour
    app.config['SESSION_COOKIE_SECURE'] = False  # Set to True in production with HTTPS
    app.config['SESSION_COOKIE_HTTPONLY'] = True
    app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'

    with app.app_context():
        from app.routes import main
        app.register_blueprint(main.main)
        
        return app 