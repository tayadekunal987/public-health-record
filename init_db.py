import sqlite3
import os
from werkzeug.security import generate_password_hash

DATABASE = 'instance/site.db'

def init_db():
    if not os.path.exists('instance'):
        os.makedirs('instance')
        
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    # Create User Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT NOT NULL,
            is_active BOOLEAN DEFAULT 1,
            
            -- Profile Fields
            age INTEGER,
            gender TEXT,
            blood_group TEXT,
            contact_number TEXT,
            address TEXT,
            medical_notes TEXT,
            
            -- Doctor Specific
            specialization TEXT,
            experience_years INTEGER,
            available_time TEXT,
            available_slots TEXT
        )
    ''')
    
    # Create Appointment Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS appointment (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_id INTEGER NOT NULL,
            doctor_id INTEGER NOT NULL,
            date TEXT NOT NULL,
            time TEXT NOT NULL,
            status TEXT DEFAULT 'Pending',
            rejection_reason TEXT,
            notification_msg TEXT,
            notification_read BOOLEAN DEFAULT 0,
            
            -- Consultation Details
            symptoms TEXT,
            diagnosis TEXT,
            advice TEXT,
            prescription TEXT,
            completed_at TIMESTAMP,
            
            FOREIGN KEY(patient_id) REFERENCES user(id),
            FOREIGN KEY(doctor_id) REFERENCES user(id)
        )
    ''')

    # Create Contact Message Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS contact_message (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            subject TEXT NOT NULL,
            message TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            is_read BOOLEAN DEFAULT 0
        )
    ''')

    # Create Announcement Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS announcement (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            content TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            created_by INTEGER,
            FOREIGN KEY (created_by) REFERENCES user (id)
        )
    ''')
    
    
    # Create Default Admin if not exists
    cursor.execute("SELECT * FROM user WHERE role = 'admin'")
    if not cursor.fetchone():
        hashed_pw = generate_password_hash('admin123', method='scrypt')
        cursor.execute('''
            INSERT INTO user (name, email, password, role, is_active)
            VALUES (?, ?, ?, ?, ?)
        ''', ('Super Admin', 'admin@example.com', hashed_pw, 'admin', 1))
        print("Default Admin created: admin@example.com / admin123")

    conn.commit()
    conn.close()
    print("Database initialized successfully.")

if __name__ == '__main__':
    init_db()
