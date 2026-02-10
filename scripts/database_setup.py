import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(BASE_DIR)
DB_PATH = os.path.join(PROJECT_ROOT, 'data', 'solar_brain.db')

def create_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS measurements (
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
               irradiance REAL,
               temperature REAL,
               power REAL
               )
         ''')
    
    conn.commit()
    conn.close()
    print(f"Database and table setup complete.")

if __name__ == "__main__":
    create_db()


