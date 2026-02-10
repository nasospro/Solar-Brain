import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(BASE_DIR)
DB_PATH = os.path.join(PROJECT_ROOT, 'data', 'solar_brain.db')


def add_prediction_column():
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        cursor.execute("ALTER TABLE measurements ADD COLUMN predicted_power REAL")
        conn.commit()
        print(f"Success: Column 'predicted_power' added successfully in {DB_PATH}!")
        
    except sqlite3.OperationalError as e:
        if "duplicate column name" in str(e):
            print("Notice: Column 'predicted_power' already exists.")
        else:
            print(f"Error: {e}")
    
    finally:
        if 'conn' in locals():
            conn.close()

if __name__ == "__main__":
    add_prediction_column()