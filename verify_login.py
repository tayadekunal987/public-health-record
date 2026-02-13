from app import app, User, load_user
from werkzeug.security import check_password_hash
from database import get_db

def test_admin_login():
    with app.app_context():
        db = get_db()
        users = db.execute("SELECT * FROM user WHERE email='admin@example.com'").fetchall()
        
        print(f"Found {len(users)} admin user(s).")
        
        if not users:
            print("No admin user found.")
            return

        user_row = users[0]
        print(f"Found admin user: {user_row['email']}")
        print(f"Stored Hash: {user_row['password']}")
        print(f"Role: {user_row['role']}")
        print(f"Is Active (Raw DB): {user_row['is_active']} (Type: {type(user_row['is_active'])})")
        
        # Test Password
        is_valid = check_password_hash(user_row['password'], 'admin123')
        print(f"Password Check ('admin123'): {is_valid}")
        
        if not is_valid:
            print("WARNING: Password check failed.")
        else:
            print("Password check passed.")

        # Test User Instantiation (simulate login_user)
        try:
            user_obj = User.get(user_row['id'])
            if user_obj:
                print(f"User Object Created Successfully. ID: {user_obj.id}")
                print(f"User.is_active Property: {user_obj.is_active}")
            else:
                print("User.get returned None!")
        except Exception as e:
            print(f"CRITICAL ERROR instantiating User object: {e}")
            import traceback
            traceback.print_exc()

if __name__ == '__main__':
    test_admin_login()
