import sqlite3

conn = sqlite3.connect('solar_brain.db') 
cursor = conn.cursor()

try:
    cursor.execute("ALTER TABLE measurements ADD COLUMN predicted_power REAL")
    conn.commit()
    print("Column 'predicted_power' added successfully!")
except sqlite3.OperationalError:
    print("Column 'predicted_power' already exists.")

conn.close()