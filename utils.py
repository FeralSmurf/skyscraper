# utils.py
from datetime import datetime

def validate_date(date_str):
    try:
        # Handle different date formats
        date_str = date_str.replace('.', '-').replace(' ', '-').replace('/', '-')

        # Check if the date string is in the correct format
        datetime.strptime(date_str, "%Y-%m-%d")

        # Make sure the date is in the future
        if datetime.strptime(date_str, "%Y-%m-%d") < datetime.now():
            return False

        return True
    except ValueError:
        return False