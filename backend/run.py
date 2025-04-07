"""
Main entry point for the Voting App.
"""

from backend import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True) 