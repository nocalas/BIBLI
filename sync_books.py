import logging
from datetime import datetime
import requests
from io import StringIO
import csv
from config import (
    CURRENTLY_READING_URL,
    READING_HISTORY_URL
)

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def fetch_sheet_data(url):
    """Fetch data from a public Google Sheet using direct URL"""
    try:
        response = requests.get(url)
        response.raise_for_status()
        logger.info(f"Successfully fetched data from {url}")
        
        # Strip any BOM markers and clean the response text
        clean_text = response.text.strip().lstrip('\ufeff')
        if not clean_text:
            logger.warning("Empty response from sheet")
            return []

        # Parse CSV response
        csv_file = StringIO(clean_text)
        reader = csv.reader(csv_file)
        next(reader)  # Skip header row
        parsed_lines = list(reader)
        logger.info(f"Parsed {len(parsed_lines)} rows from sheet")
        return parsed_lines
    except Exception as e:
        logger.error(f"Error fetching sheet data: {e}")
        return []

def sync_books():
    """Sync books from both Google Sheets"""
    logger.info(f"Starting book sync at {datetime.now()}")
    
    # Fetch current book
    current_book_data = fetch_sheet_data(CURRENTLY_READING_URL)
    if current_book_data:
        logger.info("Successfully fetched current book data")
    else:
        logger.warning("No current book data found")

    # Fetch reading history
    history_data = fetch_sheet_data(READING_HISTORY_URL)
    if history_data:
        logger.info(f"Successfully fetched {len(history_data)} books from reading history")
    else:
        logger.warning("No reading history data found")

    logger.info("Book sync completed")

if __name__ == "__main__":
    sync_books()
