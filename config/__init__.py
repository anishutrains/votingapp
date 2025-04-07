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
    DB_HOST = 'localhost'
    DB_PORT = 5432
    DB_NAME = 'postgres'  # Changed to match your existing database name
    DB_USER = 'postgres'
    DB_PASSWORD = 'admin'  # Update this to match your PostgreSQL password
    
    # Static files
    STATIC_FOLDER = 'static'
    TEMPLATES_FOLDER = 'templates'
    
    # Session settings
    SESSION_TYPE = 'filesystem'
    PERMANENT_SESSION_LIFETIME = 3600  # 1 hour

    # Connection string for psycopg2
    DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}" 