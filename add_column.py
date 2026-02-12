import sqlite3

# Connect to the database
conn = sqlite3.connect('instance/site.db')
cursor = conn.cursor()

# Check if the column already exists to avoid errors
cursor.execute("PRAGMA table_info(appointment)")
columns = [info[1] for info in cursor.fetchall()]

if 'rejection_reason' not in columns:
    print("Adding 'rejection_reason' column to 'appointment' table...")
    cursor.execute("ALTER TABLE appointment ADD COLUMN rejection_reason TEXT")
    conn.commit()
    print("Column added successfully.")
else:
    print("'rejection_reason' column already exists.")

conn.close()
