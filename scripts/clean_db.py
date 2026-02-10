import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(BASE_DIR)
DB_PATH = os.path.join(PROJECT_ROOT, 'data', 'solar_brain.db')

def clean_database():
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        cursor.execute('DELETE FROM measurements')
        cursor.execute("DELETE FROM sqlite_sequence WHERE name='measurements'")

        conn.commit()
        conn.close()
        print("Data cleaned!")

    except sqlite3.OperationalError as e:
        print(f"Error: Could not find or open database at {DB_PATH}. {e}")

if __name__ == "__main__":
    clean_database()






        

