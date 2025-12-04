"""
To run: python test_user.py
"""

from planner.user import User
import json

def main():
    print("=" * 50)
    print("TESTING USER MANAGEMENT SYSTEM")
    print("=" * 50)
    
    user_manager = User()
    
    # Test 1
    print("\n1. Creating a new user...")
    create_request = json.dumps({
        "name": "Bilal_Shaikh",
        "display_name": "Bilal Shaikh"
    })
    
    try:
        response = user_manager.create_user(create_request)
        print(f"✓ User created successfully!")
        print(f"Response: {response}")
    except Exception as e:
        print(f"✗ Error: {e}")
    
    # Test 2
    print("\n2. Creating another user...")
    create_request2 = json.dumps({
        "name": "Ravi_gupta",
        "display_name": "Ravi Gupta"
    })
    
    try:
        response = user_manager.create_user(create_request2)
        print(f"✓ User created successfully!")
        print(f"Response: {response}")
    except Exception as e:
        print(f"✗ Error: {e}")
    
     # Test 3
    print("\n3. Listing all users...")
    try:
        users_list = user_manager.list_users()
        print("✓ Users retrieved successfully!")
        print(users_list)
    except Exception as e:
        print(f"✗ Error: {e}")
    
        # Test 4
    print("\n4. Getting details of user_1...")
    describe_request = json.dumps({
        "id": "user_1"
    })
    
    try:
        user_details = user_manager.describe_user(describe_request)
        print("✓ User details retrieved!")
        print(user_details)
    except Exception as e:
        print(f"✗ Error: {e}")
    
# Test 5
    print("\n5. Updating user_1's display name...")
    update_request = json.dumps({
        "id": "user_1",
        "user": {
            "display_name": "Ahmed Ahmed Shaikh"
        }
    })
    
    try:
        response = user_manager.update_user(update_request)
        print("✓ User updated successfully!")
        print(response)
    except Exception as e:
        print(f"✗ Error: {e}")
    
    # Test 6
    print("\n6. Verifying the update...")
    try:
        user_details = user_manager.describe_user(describe_request)
        print(user_details)
    except Exception as e:
        print(f"✗ Error: {e}")
    
    # Test 7
    print("\n7. Testing constraint: Trying to create duplicate user...")
    duplicate_request = json.dumps({
        "name": "Bilal_Shaikh", 
        "display_name": "Bilal Shaikh"
    })
    
    try:
        response = user_manager.create_user(duplicate_request)
        print(f"✗ Duplicate user was created (this shouldn't happen!)")
    except Exception as e:
        print(f"✓ Correctly rejected duplicate: {e}")
    
    print("\n" + "=" * 50)
    print("TESTS COMPLETED!")
    print("=" * 50)
    print("\nCheck the 'db' folder - you'll see a users.json file")
    print("This is where all user data is stored!")

if __name__ == "__main__":
    main()