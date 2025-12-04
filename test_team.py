"""
To run: python test_team.py
"""

from planner.user import User
from planner.team import Team
import json

def main():
    print("=" * 50)
    print("TESTING TEAM MANAGEMENT SYSTEM")
    print("=" * 50)
    
    
    user_manager = User()
    team_manager = Team()
    
    print("\n📋 SETUP: Creating users first...")
    
    users_to_create = [
        {"name": "alice_wonder", "display_name": "Alice Wonderland"},
        {"name": "bob_builder", "display_name": "Bob The Builder"},
        {"name": "charlie_chaplin", "display_name": "Charlie Chaplin"},
        {"name": "diana_prince", "display_name": "Diana Prince"}
    ]
    
    created_users = []
    for user_data in users_to_create:
        try:
            response = user_manager.create_user(json.dumps(user_data))
            user_id = json.loads(response)["id"]
            created_users.append(user_id)
            print(f"✓ Created user: {user_data['display_name']} ({user_id})")
        except Exception as e:

            print(f"  User {user_data['name']} already exists (that's fine!)")
            
            created_users.append(f"user_{len(created_users) + 1}")
    
    print("\n" + "=" * 50)
    print("PART 1: CREATING TEAMS")
    print("=" * 50)
    
    
    print("\n1. Creating 'Backend Team'...")
    create_team_request = json.dumps({
        "name": "Backend Team",
        "description": "Handles all backend services and APIs",
        "admin": "user_1"  
    })
    
    try:
        response = team_manager.create_team(create_team_request)
        team_id = json.loads(response)["id"]
        print(f"✓ Team created successfully! Team ID: {team_id}")
    except Exception as e:
        print(f"✗ Error: {e}")
    
    print("\n2. Creating 'Frontend Team'...")
    create_team_request2 = json.dumps({
        "name": "Frontend Team",
        "description": "Works on UI/UX and client-side code",
        "admin": "user_2" 
    })
    
    try:
        response = team_manager.create_team(create_team_request2)
        team_id2 = json.loads(response)["id"]
        print(f"✓ Team created successfully! Team ID: {team_id2}")
    except Exception as e:
        print(f"✗ Error: {e}")
    
    print("\n" + "=" * 50)
    print("PART 2: LISTING AND DESCRIBING TEAMS")
    print("=" * 50)
    
    print("\n3. Listing all teams...")
    try:
        teams_list = team_manager.list_teams()
        print("✓ Teams retrieved successfully!")
        print(teams_list)
    except Exception as e:
        print(f"✗ Error: {e}")
    
    print("\n4. Getting details of team_1...")
    describe_request = json.dumps({"id": "team_1"})
    
    try:
        team_details = team_manager.describe_team(describe_request)
        print("✓ Team details retrieved!")
        print(team_details)
    except Exception as e:
        print(f"✗ Error: {e}")
    
    print("\n" + "=" * 50)
    print("PART 3: MANAGING TEAM MEMBERS")
    print("=" * 50)
    
    print("\n5. Adding Charlie and Diana to Backend Team...")
    add_users_request = json.dumps({
        "id": "team_1",
        "users": ["user_3", "user_4"]
    })
    
    try:
        response = team_manager.add_users_to_team(add_users_request)
        print("✓ Users added to team successfully!")
        print(json.loads(response)["message"])
    except Exception as e:
        print(f"✗ Error: {e}")
    
    print("\n6. Listing all members of Backend Team...")
    list_users_request = json.dumps({"id": "team_1"})
    
    try:
        members = team_manager.list_team_users(list_users_request)
        print("✓ Team members retrieved!")
        print(members)
    except Exception as e:
        print(f"✗ Error: {e}")
    
    print("\n7. Removing Charlie from Backend Team...")
    remove_users_request = json.dumps({
        "id": "team_1",
        "users": ["user_3"]
    })
    
    try:
        response = team_manager.remove_users_from_team(remove_users_request)
        print("✓ User removed successfully!")
    except Exception as e:
        print(f"✗ Error: {e}")
    
    print("\n8. Verifying team members after removal...")
    try:
        members = team_manager.list_team_users(list_users_request)
        print(members)
    except Exception as e:
        print(f"✗ Error: {e}")
    
    print("\n" + "=" * 50)
    print("PART 4: UPDATING TEAMS")
    print("=" * 50)
    
    print("\n9. Updating Backend Team description...")
    update_request = json.dumps({
        "id": "team_1",
        "team": {
            "description": "Backend services, APIs, and database management"
        }
    })
    
    try:
        response = team_manager.update_team(update_request)
        print("✓ Team updated successfully!")
        
        # Verify the update
        team_details = team_manager.describe_team(describe_request)
        print("Updated details:")
        print(team_details)
    except Exception as e:
        print(f"✗ Error: {e}")
    
    print("\n" + "=" * 50)
    print("PART 5: TESTING CONSTRAINTS")
    print("=" * 50)
    
    print("\n10. Testing: Creating duplicate team name...")
    duplicate_request = json.dumps({
        "name": "Backend Team", 
        "description": "Another backend team",
        "admin": "user_1"
    })
    
    try:
        response = team_manager.create_team(duplicate_request)
        print("✗ Duplicate team was created (shouldn't happen!)")
    except Exception as e:
        print(f"✓ Correctly rejected duplicate: {e}")
    
    print("\n11. Testing: Trying to remove admin from their team...")
    remove_admin_request = json.dumps({
        "id": "team_1",
        "users": ["user_1"]  
    })
    
    try:
        response = team_manager.remove_users_from_team(remove_admin_request)
        print("✗ Admin was removed (shouldn't happen!)")
    except Exception as e:
        print(f"✓ Correctly prevented admin removal: {e}")
    
    print("\n" + "=" * 50)
    print("PART 6: USER-TEAM RELATIONSHIP")
    print("=" * 50)
    
    print("\n12. Checking which teams user_1 (Alice) belongs to...")
    user_teams_request = json.dumps({"id": "user_1"})
    
    try:
        user_teams = user_manager.get_user_teams(user_teams_request)
        print("✓ User's teams retrieved!")
        print(user_teams)
    except Exception as e:
        print(f"✗ Error: {e}")
    
    print("\n" + "=" * 50)
    print("TESTS COMPLETED! ")
    print("=" * 50)
    print("\nCheck the 'db' folder - you'll see new files:")
    print("  • teams.json - All team data")
    print("  • team_members.json - Which users are in which teams")
    print("  • user_teams.json - Which teams each user belongs to")

if __name__ == "__main__":
    main()