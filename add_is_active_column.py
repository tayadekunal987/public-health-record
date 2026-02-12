import sqlite3

# Connect to the database
conn = sqlite3.connect('instance/site.db')
cursor = conn.cursor()

# Check user table
print("Checking 'user' table...")
cursor.execute("PRAGMA table_info(user)")
columns = [info[1] for info in cursor.fetchall()]

if 'is_active' not in columns:
    print("Adding 'is_active' column...")
    try:
        # Add column with default value 1 (True)
        cursor.execute("ALTER TABLE user ADD COLUMN is_active BOOLEAN DEFAULT 1")
        print(" - Added 'is_active' successfully.")
    except Exception as e:
        print(f" - Error adding 'is_active': {e}")
else:
    print(" - 'is_active' already exists.")

conn.commit()
conn.close()
print("\nMigration complete.")
