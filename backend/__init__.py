"""
Backend package for the Voting App.
Contains Flask application and routes.
"""

from flask import Flask
from flask_cors import CORS
from config import Config

def create_app():
    """Create and configure the Flask application."""
    app = Flask(__name__, 
                static_folder='../frontend/static',
                template_folder='../frontend/templates')
    
    # Configure the app
    app.config.from_object(Config)
    
    # Enable CORS
    CORS(app)
    
    # Register blueprints
    from .routes import main
    app.register_blueprint(main.bp)
    
    return app 