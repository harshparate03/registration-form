"""Legacy entry point.

The application now runs from app.py with Flask. Start it with:
    python app.py
"""

from app import app

if __name__ == "__main__":
    app.run(debug=True)