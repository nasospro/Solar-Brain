import sqlite3
conn = sqlite3.connect('solar_brain.db')
cursor = conn.cursor()


cursor.execute("SELECT COUNT(*) FROM measurements")
count = cursor.fetchone()[0]


cursor.execute("SELECT * FROM measurements ORDER BY id DESC LIMIT 1")
last_entry = cursor.fetchone()

conn.close()

print(f"Total entries: {count}")
print(f"Last entry: {last_entry}")