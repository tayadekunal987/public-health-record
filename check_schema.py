import sqlite3
from database import DATABASE

def check_schema():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    # Get columns for 'user' table
    cursor.execute("PRAGMA table_info(user)")
    columns = cursor.fetchall()
    
    print("Columns in 'user' table:")
    for col in columns:
        print(f"- {col[1]} ({col[2]})")
        
    conn.close()

if __name__ == '__main__':
    check_schema()
