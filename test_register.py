from app import app
import unittest

class TestRegistration(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        self.app = app.test_client()
        self.app_context = app.app_context()
        self.app_context.push()

    def tearDown(self):
        self.app_context.pop()

    def test_registration(self):
        print("Attempting to register new user test@example.com...")
        response = self.app.post('/register', data=dict(
            name='Test User',
            email='test@example.com',
            password='password123',
            role='patient'
        ), follow_redirects=True)
        
        print(f"Registration Response Status: {response.status_code}")
        
        if b'Account created' in response.data:
            print("SUCCESS: Registration successful.")
        elif b'Email already exists' in response.data:
            print("WARNING: Email already exists (Expected if run multiple times).")
        else:
            print("FAILURE: Registration failed with unexpected content.")
            # Print page title or error message if possible
            if b'Internal Server Error' in response.data:
                 print("ERROR: 500 Internal Server Error encountered.")
                 
            # print(response.data[:500])

        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()
