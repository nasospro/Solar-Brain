import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(BASE_DIR)
DB_PATH = os.path.join(PROJECT_ROOT, 'data', 'solar_brain.db')

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()


cursor.execute("SELECT COUNT(*) FROM measurements")
count = cursor.fetchone()[0]


cursor.execute("SELECT * FROM measurements ORDER BY id DESC LIMIT 1")
last_entry = cursor.fetchone()

conn.close()

print(f"Total entries: {count}")
print(f"Last entry: {last_entry}")