import os
import sys
from app.database import get_db_connection
from config import Config

def init_db():
    """Initialize the database with the schema"""
    # Create a direct connection to execute DDL statements
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        # Read the schema file
        with open('app/schema.sql', 'r') as f:
            schema = f.read()
        
        # Split the schema into individual statements
        statements = schema.split(';')
        
        # Execute each statement
        for statement in statements:
            # Skip empty statements
            if not statement.strip():
                continue
            
            try:
                cursor.execute(statement)
                print(f"Executed: {statement[:50]}...")
            except Exception as e:
                print(f"Error executing statement: {statement[:50]}...")
                print(f"Error details: {e}")
                # Continue with other statements even if one fails
                continue
        
        # Commit the transaction
        conn.commit()
        print("Database schema created successfully.")
        
        # Verify tables were created
        cursor.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
        """)
        tables = [row[0] for row in cursor.fetchall()]
        print(f"Created tables: {', '.join(tables)}")
        
    except Exception as e:
        print(f"Error initializing database: {e}")
        conn.rollback()
        sys.exit(1)
    finally:
        conn.close()

if __name__ == '__main__':
    # Create static/images directory if it doesn't exist
    os.makedirs('static/images', exist_ok=True)
    
    # Initialize the database
    init_db()
    print("Database initialization completed.") 