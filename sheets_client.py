import logging
from datetime import datetime
import requests
from io import StringIO
import csv
from config import CACHE_TIMEOUT, CURRENTLY_READING_URL, READING_HISTORY_URL, NEXT_UP_URL

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def get_sheet_data(url):
    """Fetch data from a public Google Sheet using direct URL"""
    try:
        response = requests.get(url)
        response.raise_for_status()
        logger.debug(f"Raw response from URL: {response.text}")

        # Strip any BOM markers and clean the response text
        clean_text = response.text.strip().lstrip('\ufeff')
        if not clean_text:
            logger.warning("Empty response from sheet")
            return []

        # Parse CSV response
        try:
            csv_file = StringIO(clean_text)
            reader = csv.reader(csv_file)
            next(reader)  # Skip header row
            parsed_lines = list(reader)
            logger.debug(f"Parsed data from sheet: {parsed_lines}")
            return parsed_lines
        except Exception as e:
            logger.error(f"Error parsing CSV data: {e}")
            return []
    except Exception as e:
        logger.error(f"Error fetching sheet data: {e}")
        return []

def fetch_current_book(timestamp=None):
    """Fetch current book with caching"""
    if timestamp is None:
        timestamp = datetime.now().timestamp() // CACHE_TIMEOUT

    try:
        response = requests.get(CURRENTLY_READING_URL)
        if response.status_code != 200:
            logger.error(f"Failed to fetch sheet: {response.status_code}")
            return None

        raw_data = response.text
        csv_reader = csv.reader(StringIO(raw_data))
        rows = [row for row in csv_reader if row]

        if rows and len(rows[0]) >= 4:
            title = rows[0][0].strip('" ')
            author = rows[0][1].strip('" ')
            wiki_link = rows[0][2].strip('" ')
            image_url = rows[0][3].strip('" ') if len(rows[0]) > 3 else None
            return {
                "title": title,
                "author": author,
                "wiki_link": wiki_link,
                "image_url": image_url
            }

        logger.warning("No valid data found in Currently Reading sheet")
        return None
    except Exception as e:
        logger.error(f"Error processing current book data: {e}")
        return None

def fetch_reading_history(timestamp=None):
    """Fetch reading history with caching"""
    if timestamp is None:
        timestamp = datetime.now().timestamp() // CACHE_TIMEOUT

    try:
        values = get_sheet_data(READING_HISTORY_URL)
        logger.debug(f"Processing {len(values)} reading history entries")
        history = {}

        # Initialize 2025 with empty list to ensure it appears even if no books
        history['2025'] = []

        for row in values:
            if len(row) >= 4:  # Ensure we have title, author, year, and wiki_link
                title = row[0].strip('" ')
                author = row[1].strip('" ')
                year = row[2].strip('" ') or str(datetime.now().year)  # Use current year if empty
                wiki_link = row[3].strip('" ')

                logger.debug(f"Processing book: {title} by {author} ({year})")
                if year not in history:
                    history[year] = []

                history[year].append({
                    'title': title,
                    'author': author,
                    'wiki_link': wiki_link
                })

        # Sort years in reverse chronological order
        sorted_history = dict(sorted(history.items(), key=lambda x: x[0], reverse=True))
        logger.debug(f"Final history structure: {sorted_history}")
        return sorted_history
    except Exception as e:
        logger.error(f"Error processing reading history: {e}")
        return {'2025': []}  # Return empty 2025 list as fallback

def fetch_next_up_books(timestamp=None):
    """Fetch next up books with caching"""
    if timestamp is None:
        timestamp = datetime.now().timestamp() // CACHE_TIMEOUT

    try:
        response = requests.get(NEXT_UP_URL)
        if response.status_code != 200:
            logger.error(f"Failed to fetch Next Up sheet: {response.status_code}")
            return []

        # Parse CSV data directly from response
        csv_file = StringIO(response.text)
        reader = csv.DictReader(csv_file)
        next_up_books = []

        for row in reader:
            try:
                logger.debug(f"Processing next up book row: {row}")
                next_up_books.append({
                    'title': row.get('Title', '').strip(),
                    'author': row.get('Author', '').strip(),
                    'wiki_link': row.get('Wikipedia Link', '').strip(),
                    'image_url': row.get('Image URL', '').strip()
                })
            except Exception as e:
                logger.error(f"Error processing next up book row: {e}")
                continue

        logger.info(f"Successfully fetched {len(next_up_books)} next up books")
        return next_up_books
    except Exception as e:
        logger.error(f"Error processing next up books: {e}")
        return []