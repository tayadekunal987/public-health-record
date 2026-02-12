from app import app, User
from werkzeug.security import check_password_hash
import sys

def test_login(email, password):
    print(f"Testing login for {email}...")
    with app.app_context():
        # 1. Test fetching user
        try:
            print("Fetching user by email...")
            user = User.get_by_email(email)
            if not user:
                print("User not found in DB.")
                return
            print(f"User found: ID={user.id}, Role={user.role}, Name={user.name}")
        except Exception as e:
            print(f"CRASH in User.get_by_email: {e}")
            import traceback
            traceback.print_exc()
            return

        # 2. Test Password Check
        try:
            print("Checking password...")
            # Note: stored password hash might be scrypt or pbkdf2 depending on when it was created
            print(f"Stored Hash: {user.password[:20]}...")
            if check_password_hash(user.password, password):
                print("Password Match: YES")
            else:
                print("Password Match: NO")
        except Exception as e:
            print(f"CRASH in check_password_hash: {e}")
            traceback.print_exc()
            return

        # 3. Test Active Check
        try:
            print(f"Is Active: {user.is_active}")
            if not user.is_active:
                print("User is deactivated.")
            else:
                print("User is active.")
        except Exception as e:
            print(f"Error checking is_active: {e}")

if __name__ == "__main__":
    # Test with the admin user we created or found
    test_login('admin@example.com', 'admin123')
    
    # Try the user found in previous step (ID 1: KUNAL TAYADE)
    # I don't know the password, but testing the retrieval part is key.
    # I'll just try to fetch him.
    print("\n--- Testing Retrieval Only for ID 1 ---")
    with app.app_context():
        u = User.get(1)
        if u:
            print(f"Successfully retrieved user {u.name}")
        else:
            print("Failed to retrieve user 1")
