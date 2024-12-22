import os

# Google Sheets Configuration
CURRENT_READING_SPREADSHEET_ID = '1NWBBveV6wwAXOqmDXJGuQWpe9s4WM19chVosOgUo3Xs'
READING_HISTORY_SPREADSHEET_ID = '1sO8J6OgTKrwy3WLqfmfyBNsggT4AIgGb158cZAGiy2A'
NEXT_UP_SPREADSHEET_ID = '2PACX-1vRQvQThwkZ9omH6rfvrom9AmaSUHE7Cf7uiwY97pSh6JBCsPqef073SUethxqfKzbNzqso8Uji3x5_v'

# Updated URLs to use the published format for Next Up
CURRENTLY_READING_URL = f"https://docs.google.com/spreadsheets/d/{CURRENT_READING_SPREADSHEET_ID}/gviz/tq?tqx=out:csv&sheet=Currently%20Reading&range=A2:D"
READING_HISTORY_URL = f"https://docs.google.com/spreadsheets/d/{READING_HISTORY_SPREADSHEET_ID}/gviz/tq?tqx=out:csv&sheet=Reading%20History&range=A2:D"
NEXT_UP_URL = f"https://docs.google.com/spreadsheets/d/e/{NEXT_UP_SPREADSHEET_ID}/pub?gid=0&single=true&output=csv"

# Cache Configuration
CACHE_TIMEOUT = 300  # 5 minutes

# Flask Configuration
SECRET_KEY = os.environ.get('FLASK_SECRET_KEY', 'your-secret-key-here')
DEBUG = True