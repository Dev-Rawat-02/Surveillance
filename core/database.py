import sqlite3

class DatabaseManager:

    def __init__(self):
        self.connection = sqlite3.connect("database/surveillance.db")
        self.connection.row_factory = sqlite3.Row
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

    def fetch_alerts(self, limit=100):

        self.cursor.execute("""
            SELECT id, timestamp, label, confidence, snapshot
            FROM alerts
            ORDER BY id DESC
            LIMIT ?
        """, (limit,))

        rows = self.cursor.fetchall()
        return [dict(row) for row in rows]

    def count_alerts(self):

        self.cursor.execute("SELECT COUNT(*) AS total FROM alerts")
        row = self.cursor.fetchone()
        return int(row["total"]) if row else 0