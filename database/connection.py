"""
Database connection module for the Voting App.

This module handles the connection to the PostgreSQL database.
"""

import pg8000
from config import Config

def get_db_connection():
    """Create a PostgreSQL database connection"""
    try:
        conn = pg8000.connect(
            host=Config.DB_HOST,
            user=Config.DB_USER,
            password=Config.DB_PASSWORD,
            port=int(Config.DB_PORT),
            database=Config.DB_NAME
        )
        return conn
    except Exception as e:
        print(f"Error connecting to PostgreSQL: {e}")
        raise e

def execute_query(query, params=None, fetch=False):
    """Execute a SQL query and optionally fetch results"""
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        
        # Convert SQLite-style placeholders to PostgreSQL style if needed
        if params:
            query = query.replace('?', '%s')
            
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
            
        if fetch:
            # pg8000 returns tuples, convert to dict-like objects
            columns = [desc[0] for desc in cursor.description]
            return [dict(zip(columns, row)) for row in cursor.fetchall()]
        
        conn.commit()
        return cursor.rowcount
    except Exception as e:
        conn.rollback()
        print(f"Database error: {e}")
        raise e
    finally:
        conn.close() 