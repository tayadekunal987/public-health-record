import sqlite3
import sqlalchemy

# Connect to the database
conn = sqlite3.connect('instance/site.db')
cursor = conn.cursor()

# Get existing columns
print("Checking 'appointment' table...")
cursor.execute("PRAGMA table_info(appointment)")
columns = [info[1] for info in cursor.fetchall()]

new_columns = {
    'symptoms': 'TEXT',
    'diagnosis': 'TEXT',
    'advice': 'TEXT',
    'prescription': 'TEXT',
    'completed_at': 'TIMESTAMP'
}

for col_name, col_type in new_columns.items():
    if col_name not in columns:
        print(f"Adding '{col_name}'...")
        try:
            cursor.execute(f"ALTER TABLE appointment ADD COLUMN {col_name} {col_type}")
            print(f" - Added '{col_name}' successfully.")
        except Exception as e:
            print(f" - Error adding '{col_name}': {e}")
    else:
        print(f" - '{col_name}' already exists.")

conn.commit()
conn.close()
print("\nMigration complete.")
