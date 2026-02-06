import sqlite3
conn = sqlite3.connect('solar_brain.db')
cursor = conn.cursor()

cursor.execute('DELETE FROM measurements')
cursor.execute("DELETE FROM sqlite_sequence WHERE name='measurements'")

conn.commit()
conn.close()
print("Data cleaned!")