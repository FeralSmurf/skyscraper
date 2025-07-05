import sqlite3
from datetime import datetime

# Get the current day and time
now = datetime.now()
search_date = now.strftime("%Y-%m-%d %H:%M:%S")
search_time = now.strftime("%H:%M:%S")


def create_db():
    conn = sqlite3.connect("/home/feralsmurf/Desktop/skyscraper/flights.db")
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS searches (
            id INTEGER PRIMARY KEY,
            search_date TEXT NOT NULL,
            search_time TEXT NOT NULL,
            from_airport TEXT NOT NULL,
            to_airport TEXT NOT NULL,
            departure_date TEXT NOT NULL,
            return_date TEXT NOT NULL,
            price TEXT,
            departure_hour TEXT,
            return_hour TEXT
        )
    """)

    conn.commit()
    conn.close()


def insert_data(
    from_airport,
    to_airport,
    departure_date,
    return_date,
    price,
    departure_hour,
    return_hour,
):
    # Generate search_date and search_time
    search_date = datetime.now().strftime("%Y-%m-%d")
    search_time = datetime.now().strftime("%H:%M:%S")

    conn = sqlite3.connect("/home/feralsmurf/Desktop/skyscraper/flights.db")
    c = conn.cursor()
    c.execute(
        """
        INSERT INTO searches (search_date, search_time, from_airport, to_airport, departure_date, return_date, price, departure_hour, return_hour)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """,
        (
            search_date,
            search_time,
            from_airport,
            to_airport,
            departure_date,
            return_date,
            price,
            departure_hour,
            return_hour,
        ),
    )
    conn.commit()
    conn.close()
    print("🥳🥳🥳 Data inserted successfully! 🌠🌠🌠")
