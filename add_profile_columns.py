import sqlite3

# Connect to the database
conn = sqlite3.connect('instance/site.db')
cursor = conn.cursor()

# Get existing columns
cursor.execute("PRAGMA table_info(user)")
columns = [info[1] for info in cursor.fetchall()]

# Define new columns
new_columns = {
    'age': 'INTEGER',
    'gender': 'TEXT',
    'blood_group': 'TEXT',
    'contact_number': 'TEXT',
    'address': 'TEXT',
    'specialization': 'TEXT',
    'experience_years': 'INTEGER',
    'available_time': 'TEXT',
    'medical_notes': 'TEXT'
}

print("Checking and adding columns to 'user' table...")

for col_name, col_type in new_columns.items():
    if col_name not in columns:
        print(f"Adding '{col_name}' ({col_type})...")
        try:
            cursor.execute(f"ALTER TABLE user ADD COLUMN {col_name} {col_type}")
            print(f" - Added '{col_name}' successfully.")
        except Exception as e:
            print(f" - Error adding '{col_name}': {e}")
    else:
        print(f" - Column '{col_name}' already exists.")

conn.commit()
conn.close()
print("Migration complete.")
