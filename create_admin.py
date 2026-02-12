import sqlite3
from werkzeug.security import generate_password_hash

DATABASE = 'instance/site.db'

def create_admin():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    # Check if admin already exists
    cursor.execute("SELECT * FROM user WHERE role = 'admin'")
    admin = cursor.fetchone()
    
    if not admin:
        hashed_password = generate_password_hash('admin123', method='scrypt')
        cursor.execute('''
            INSERT INTO user (name, email, password, role, is_active)
            VALUES (?, ?, ?, ?, ?)
        ''', ('System Admin', 'admin@example.com', hashed_password, 'admin', True))
        
        conn.commit()
        print("Admin user created successfully.")
        print("Email: admin@example.com")
        print("Password: admin123")
    else:
        print("Admin user already exists.")
    
    conn.close()

if __name__ == '__main__':
    create_admin()
