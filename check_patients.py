import sqlite3

try:
    conn = sqlite3.connect('instance/site.db')
    cursor = conn.cursor()
    cursor.execute("SELECT email FROM user WHERE role='patient'")
    patients = cursor.fetchall()
    conn.close()
    
    if patients:
        print("Found patients:")
        for p in patients:
            print(f"- {p[0]}")
    else:
        print("No patient users found.")
except Exception as e:
    print(f"Error: {e}")
