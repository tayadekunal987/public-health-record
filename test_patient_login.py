from app import app, User
import unittest

class TestPatientLogin(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        self.app = app.test_client()
        self.app_context = app.app_context()
        self.app_context.push()

    def tearDown(self):
        self.app_context.pop()

    def test_patient_flow(self):
        # 1. Register
        email = 'patient_test_flow@example.com'
        password = 'password123'
        print(f"Registering {email}...")
        reg_res = self.app.post('/register', data=dict(
            name='Test Patient',
            email=email,
            password=password,
            role='patient'
        ), follow_redirects=True)
        
        self.assertEqual(reg_res.status_code, 200)
        if b'Account created' not in reg_res.data and b'Email already exists' not in reg_res.data:
            print("FAILURE: Registration failed.")
            print(reg_res.data[:500])
            return

        # 2. Login
        print("Attempting login...")
        login_res = self.app.post('/login', data=dict(
            email=email,
            password=password
        ), follow_redirects=True)
        
        print(f"Login Response Status: {login_res.status_code}")
        
        if b'Welcome, Test Patient' in login_res.data or b'Patient Dashboard' in login_res.data:
            print("SUCCESS: Patient Login and Dashboard access successful.")
        elif b'Login Unsuccessful' in login_res.data:
            print("FAILURE: Login refused credentials.")
        elif b'account has been deactivated' in login_res.data:
             print("FAILURE: Account is deactivated.")
        else:
            print("FAILURE: Unexpected response.")
            # print(login_res.data[:1000])

if __name__ == '__main__':
    unittest.main()
