import os


class Config:
    DB_TYPE = 'postgres'
    # PostgreSQL connection parameters (only used if DB_TYPE is 'postgres')
    DB_HOST = 'localhost'
    DB_USER = 'postgres'
    DB_PASSWORD = 'admin'
    DB_PORT = 5432
    DB_NAME = 'postgres'
    
    # Connection string for psycopg2
    DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}" 