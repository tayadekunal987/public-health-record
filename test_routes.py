from app import app
import unittest

class TestAdminRoutes(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        self.app = app.test_client()
        self.app_context = app.app_context()
        self.app_context.push()

    def tearDown(self):
        self.app_context.pop()

    def login(self, email, password):
        return self.app.post('/login', data=dict(
            email=email,
            password=password
        ), follow_redirects=True)

    def test_admin_dashboard_access(self):
        print("Attempting login with admin@example.com...")
        response = self.login('admin@example.com', 'admin123')
        
        print(f"Login Response Status: {response.status_code}")
        
        if b'Admin Dashboard' in response.data:
            print("SUCCESS: Admin Dashboard accessed and rendered.")
        elif b'Login Unsuccessful' in response.data:
            print("FAILURE: Login failed (Invalid credentials).")
        else:
            print("FAILURE: Unexpected content. Check output below.")
            ## Print subset of response for debugging
            print(response.data[:1000])

        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()
