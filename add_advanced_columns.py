import sqlite3

# Connect to the database
conn = sqlite3.connect('instance/site.db')
cursor = conn.cursor()

# 1. Update User Table
print("Checking 'user' table...")
cursor.execute("PRAGMA table_info(user)")
user_columns = [info[1] for info in cursor.fetchall()]

if 'available_slots' not in user_columns:
    print("Adding 'available_slots' to 'user' table...")
    try:
        cursor.execute("ALTER TABLE user ADD COLUMN available_slots TEXT")
        print(" - Added 'available_slots' successfully.")
    except Exception as e:
        print(f" - Error adding 'available_slots': {e}")
else:
    print(" - 'available_slots' already exists.")

# 2. Update Appointment Table
print("\nChecking 'appointment' table...")
cursor.execute("PRAGMA table_info(appointment)")
appt_columns = [info[1] for info in cursor.fetchall()]

new_appt_cols = {
    'notification_msg': 'TEXT',
    'notification_read': 'BOOLEAN DEFAULT 0'
}

for col_name, col_type in new_appt_cols.items():
    if col_name not in appt_columns:
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
