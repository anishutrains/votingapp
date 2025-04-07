"""
Configuration settings for the Voting App.
"""

import os

class Config:
    """Base configuration class."""
    
    # Flask settings
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev')
    DEBUG = True
    
    # Database settings
    DB_TYPE = 'postgres'
    DB_HOST = os.environ.get('DB_HOST', 'localhost')
    DB_PORT = int(os.environ.get('DB_PORT', 5432))
    DB_NAME = os.environ.get('DB_NAME', 'postgres')
    DB_USER = os.environ.get('DB_USER', 'postgres')
    DB_PASSWORD = os.environ.get('DB_PASSWORD', 'admin')
    
    # Static files
    STATIC_FOLDER = 'static'
    TEMPLATES_FOLDER = 'templates'
    
    # Session settings
    SESSION_TYPE = 'filesystem'
    PERMANENT_SESSION_LIFETIME = 3600  # 1 hour

    # Connection string for psycopg2
    @property
    def DATABASE_URL(self):
        return f"postgresql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}" 