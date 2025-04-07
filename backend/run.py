"""
Main entry point for the Voting App.
"""

import os
import sys
from pathlib import Path

# Add the project root directory to Python path
project_root = str(Path(__file__).parent.parent)
sys.path.append(project_root)

from backend import create_app
from database.init_db import init_db

def setup_database():
    """Initialize the database with schema and sample data."""
    print("Initializing database...")
    if init_db():
        print("Database initialized successfully!")
    else:
        print("Error initializing database. Please check the logs.")
        sys.exit(1)

def main():
    """Main function to run the application."""
    # Initialize database
    setup_database()
    
    # Create and run Flask app
    app = create_app()
    
    # Get port from environment variable or use default
    port = int(os.environ.get('PORT', 5000))
    
    # Run the application
    app.run(host='0.0.0.0', port=port, debug=True)

if __name__ == '__main__':
    main() 