import sqlite3

class DatabaseManager:

    def __init__(self):
        self.connection = sqlite3.connect("database/surveillance.db")
        self.cursor = self.connection.cursor()

        self.create_table()

    def create_table(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS alerts(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                label TEXT,
                confidence REAL,
                snapshot TEXT
            )
        """)
        self.connection.commit()

    def save_alert(self, timestamp, label, confidence, snapshot):

        self.cursor.execute("""
            INSERT INTO alerts(timestamp, label, confidence, snapshot)
            VALUES (?, ?, ?, ?)
        """, (timestamp, label, confidence, snapshot))

        self.connection.commit()