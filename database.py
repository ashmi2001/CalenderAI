import sqlite3

def create_db():
    # Connect to SQLite database (or create it)
    conn = sqlite3.connect('meetings.db')
    cursor = conn.cursor()

    # Create a table to store meeting details
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS meetings (
        id INTEGER PRIMARY KEY,
        datetime TEXT,
        participants TEXT,
        location TEXT
    )''')

    conn.commit()
    conn.close()

def store_meeting(datetime, participants, location):
    conn = sqlite3.connect('meetings.db')
    cursor = conn.cursor()

    # Insert meeting details into the database
    cursor.execute('''
    INSERT INTO meetings (datetime, participants, location)
    VALUES (?, ?, ?)
    ''', (datetime, participants, location))

    conn.commit()
    conn.close()

def get_upcoming_meetings():
    conn = sqlite3.connect('meetings.db')
    cursor = conn.cursor()

    # Fetch upcoming meetings
    cursor.execute('SELECT * FROM meetings ORDER BY datetime LIMIT 5')
    meetings = cursor.fetchall()

    conn.close()
    return meetings
