import logging
from datetime import datetime
from flask import Flask, render_template
from sheets_client import fetch_current_book, fetch_reading_history, fetch_next_up_books
import config

app = Flask(__name__)
app.config.from_object(config)

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

@app.route('/')
def index():
    try:
        current_book = fetch_current_book()
        next_up_books = fetch_next_up_books()
        reading_history = fetch_reading_history()

        return render_template('index.html',
                             current_book=current_book,
                             next_up_books=next_up_books,
                             reading_history=reading_history,
                             current_year=datetime.now().year)
    except Exception as e:
        logger.error(f"Error in index route: {e}")
        return render_template('error.html',
                             error="Unable to load library data",
                             current_year=datetime.now().year)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('error.html',
                         error="Page not found",
                         current_year=datetime.now().year), 404

@app.errorhandler(500)
def server_error(e):
    return render_template('error.html',
                         error="Internal server error",
                         current_year=datetime.now().year), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)