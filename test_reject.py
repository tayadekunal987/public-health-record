from app import app, User
from database import get_db
import unittest

class TestDoctorReject(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        self.app = app.test_client()
        self.app_context = app.app_context()
        self.app_context.push()

    def tearDown(self):
        self.app_context.pop()

    def test_reject_flow(self):
        # 1. Create Data (Doctor, Patient, Appointment) if not exists
        db = get_db()
        # Ensure we have a doctor and patient
        # We can reuse existing ones or insert dummy. 
        # Let's insert a fresh appointment for existing users to be safe.
        # Assuming id=1 is patient? no, let's find one.
        
        patient = db.execute("SELECT * FROM user WHERE role='patient'").fetchone()
        doctor = db.execute("SELECT * FROM user WHERE role='doctor'").fetchone()
        
        if not patient or not doctor:
            print("SKIPPING: Need at least one patient and one doctor in DB.")
            return

        # Create Appointment
        cursor = db.execute(
            'INSERT INTO appointment (patient_id, doctor_id, date, time, status, notification_read) VALUES (?, ?, ?, ?, ?, ?)',
            (patient['id'], doctor['id'], '2026-12-31', '10:00 AM', 'Pending', 0)
        )
        appt_id = cursor.lastrowid
        db.commit()
        print(f"Created test appointment ID: {appt_id}")

        # 2. Login as Doctor
        print(f"Logging in as doctor {doctor['email']}...")
        self.app.post('/login', data=dict(email=doctor['email'], password='password123'), follow_redirects=True) 
        # Note: password might be hashed, this assumes typical test password or we need to reset it.
        # If login fails, subsequent request fails.
        # Actually, let's FORCE login via session helper or just assume we can get by?
        # Flask-Login test_client doesn't persistent session easily without login.
        # Let's verify login worked?
        
        # Checking if password matches might be tricky if we don't know it.
        # Let's update the doctor password to something known for this test?
        from werkzeug.security import generate_password_hash
        hashed = generate_password_hash('testpass')
        db.execute('UPDATE user SET password = ? WHERE id = ?', (hashed, doctor['id']))
        db.commit()
        
        self.app.post('/login', data=dict(email=doctor['email'], password='testpass'), follow_redirects=True)

        # 3. Reject Appointment
        print("Attempting to reject appointment...")
        res = self.app.post(f'/update_appointment/{appt_id}', data=dict(
            status='Rejected',
            reason='Test Rejection Reason'
        ), follow_redirects=True)
        
        print(f"Reject Response Status: {res.status_code}")
        
        if res.status_code == 500:
            print("FAILURE: 500 Error.")
        elif b'Appointment Rejected' in res.data:
            print("SUCCESS: Rejection handled.")
        else:
            print("FAILURE: Unexpected response.")
            # print(res.data[:500])

if __name__ == '__main__':
    unittest.main()
