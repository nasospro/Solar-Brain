import sqlite3

def create_db():
    conn = sqlite3.connect('solar_brain.db')
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


