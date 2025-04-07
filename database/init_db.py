"""
Database initialization script for the Voting App.
"""

import os
import pg8000
from config import Config

def create_database():
    """Create the database if it doesn't exist."""
    try:
        # Connect to default postgres database
        conn = pg8000.connect(
            host=Config.DB_HOST,
            user=Config.DB_USER,
            password=Config.DB_PASSWORD,
            port=int(Config.DB_PORT),
            database='postgres'
        )
        
        # Check if database exists
        with conn.cursor() as cur:
            cur.execute("SELECT 1 FROM pg_database WHERE datname = %s", (Config.DB_NAME,))
            exists = cur.fetchone()
            
            if not exists:
                # Create database
                cur.execute(f'CREATE DATABASE {Config.DB_NAME}')
                print(f"Database {Config.DB_NAME} created successfully")
            else:
                print(f"Database {Config.DB_NAME} already exists")
                
        conn.commit()
        return True
        
    except Exception as e:
        print(f"Error creating database: {str(e)}")
        return False
        
    finally:
        if conn:
            conn.close()

def init_db():
    """Initialize the database with schema and sample data."""
    # First create the database if it doesn't exist
    if not create_database():
        return False
        
    try:
        # Connect to the voting_app database
        conn = pg8000.connect(
            host=Config.DB_HOST,
            user=Config.DB_USER,
            password=Config.DB_PASSWORD,
            port=int(Config.DB_PORT),
            database=Config.DB_NAME
        )
        
        # Read schema file
        schema_path = os.path.join(os.path.dirname(__file__), 'schema.sql')
        with open(schema_path, 'r') as f:
            schema_sql = f.read()
            
        # Execute schema
        with conn.cursor() as cur:
            cur.execute(schema_sql)
            
        # Commit changes
        conn.commit()
        print("Database initialized successfully")
        return True
        
    except Exception as e:
        print(f"Error initializing database: {str(e)}")
        return False
        
    finally:
        if conn:
            conn.close()

if __name__ == '__main__':
    init_db() 