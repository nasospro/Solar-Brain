import sqlite3
conn = sqlite3.connect('solar_brain.db')
cursor = conn.cursor()

cursor.execute('DELETE FROM measurements')

conn.commit()
conn.close()
print("Database cleaned!")