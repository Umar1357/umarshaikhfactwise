"""
Test file for Project Board and Task Management
This is the complete system in action!

To run: python test_board.py
"""

from planner.user import User
from planner.team import Team
from planner.project_board import ProjectBoard
import json

def main():
    print("=" * 80)
    print("TESTING PROJECT BOARD & TASK MANAGEMENT SYSTEM")
    print("The Complete Project Planner in Action!")
    print("=" * 80)
    
    # Initialize 
    user_manager = User()
    team_manager = Team()
    board_manager = ProjectBoard()
    
    print("\n📋 SETUP: Creating users and teams...")
    
    # Create users
    users_data = [
        {"name": "Bilal_Shaikh", "display_name": "Bilal Shaikh"},
        {"name": "Ravi_gupta", "display_name": "Ravi Gupta"},
        {"name": "Alina_becker", "display_name": "Alina Becker"},
        {"name": "Hamza_Khan", "display_name": "Hamza Khan"}
    ]
    
    for user_data in users_data:
        try:
            user_manager.create_user(json.dumps(user_data))
            print(f"✓ Created user: {user_data['display_name']}")
        except:
            print(f"  User {user_data['name']} already exists")
    
    # Create ,team
    try:
        team_response = team_manager.create_team(json.dumps({
            "name": "Development Team",
            "description": "Main development team",
            "admin": "user_1"
        }))
        print(f"✓ Created Development Team")
    except:
        print("  Development Team already exists")
    
    
    try:
        team_manager.add_users_to_team(json.dumps({
            "id": "team_1",
            "users": ["user_2", "user_3", "user_4"]
        }))
        print("✓ Added members to Development Team")
    except:
        print("  Members already added")
    
    print("\n" + "=" * 80)
    print("PART 1: CREATING PROJECT BOARDS")
    print("=" * 80)
    
    print("\n1. Creating 'Sprint 1' board...")
    create_board_request = json.dumps({
        "name": "Sprint 1",
        "description": "First sprint - Authentication features",
        "team_id": "team_1"
    })
    
    try:
        response = board_manager.create_board(create_board_request)
        board_id = json.loads(response)["id"]
        print(f"✓ Board created successfully! Board ID: {board_id}")
    except Exception as e:
        print(f"✗ Error: {e}")
    
    print("\n2. Creating 'Sprint 2' board...")
    create_board_request2 = json.dumps({
        "name": "Sprint 2",
        "description": "Second sprint - User dashboard",
        "team_id": "team_1"
    })
    
    try:
        response = board_manager.create_board(create_board_request2)
        board_id2 = json.loads(response)["id"]
        print(f"✓ Board created successfully! Board ID: {board_id2}")
    except Exception as e:
        print(f"✗ Error: {e}")
    
    print("\n" + "=" * 80)
    print("PART 2: ADDING TASKS TO BOARDS")
    print("=" * 80)
    
    tasks_sprint1 = [
        {
            "title": "Design login page",
            "description": "Create wireframes and mockups for login",
            "user_id": "user_1",
            "board_id": "board_1"
        },
        {
            "title": "Implement login API",
            "description": "Create REST API endpoints for authentication",
            "user_id": "user_2",
            "board_id": "board_1"
        },
        {
            "title": "Write unit tests",
            "description": "Test coverage for authentication module",
            "user_id": "user_3",
            "board_id": "board_1"
        },
        {
            "title": "Setup database schema",
            "description": "Create users table and indexes",
            "user_id": "user_4",
            "board_id": "board_1"
        }
    ]
    
    print("\n3. Adding tasks to Sprint 1 board...")
    for i, task_data in enumerate(tasks_sprint1, 1):
        try:
            response = board_manager.add_task(json.dumps(task_data))
            task_id = json.loads(response)["id"]
            print(f"✓ Task {i}: '{task_data['title']}' added ({task_id})")
        except Exception as e:
            print(f"✗ Error adding task {i}: {e}")
    
    print("\n" + "=" * 80)
    print("PART 3: UPDATING TASK STATUSES")
    print("=" * 80)
    
    print("\n4. Simulating task progress...")
    
    try:
        board_manager.update_task_status(json.dumps({
            "id": "task_1",
            "status": "COMPLETE"
        }))
        print("✓ Task 1 (Design login page) → COMPLETE")
    except Exception as e:
        print(f"✗ Error: {e}")
    
    try:
        board_manager.update_task_status(json.dumps({
            "id": "task_2",
            "status": "IN_PROGRESS"
        }))
        print("✓ Task 2 (Implement login API) → IN_PROGRESS")
    except Exception as e:
        print(f"✗ Error: {e}")
    
    
    try:
        board_manager.update_task_status(json.dumps({
            "id": "task_3",
            "status": "IN_PROGRESS"
        }))
        print("✓ Task 3 (Write unit tests) → IN_PROGRESS")
    except Exception as e:
        print(f"✗ Error: {e}")
    
    
    try:
        board_manager.update_task_status(json.dumps({
            "id": "task_4",
            "status": "COMPLETE"
        }))
        print("✓ Task 4 (Setup database schema) → COMPLETE")
    except Exception as e:
        print(f"✗ Error: {e}")
    
    print("\n" + "=" * 80)
    print("PART 4: LISTING BOARDS")
    print("=" * 80)
    
    
    print("\n5. Listing all boards for Development Team...")
    try:
        boards_list = board_manager.list_boards(json.dumps({"id": "team_1"}))
        print("✓ Boards retrieved successfully!")
        print(boards_list)
    except Exception as e:
        print(f"✗ Error: {e}")
    
    print("\n" + "=" * 80)
    print("PART 5: EXPORTING BOARD (THE COOL PART!)")
    print("=" * 80)
    
    
    print("\n6. Exporting Sprint 1 board to a beautiful text file...")
    try:
        response = board_manager.export_board(json.dumps({"id": "board_1"}))
        filename = json.loads(response)["out_file"]
        print(f"✓ Board exported successfully!")
        print(f" File created: out/{filename}")
        print("\n Go check the 'out' folder and open that file!")
        print("   It has a beautiful formatted view of your board!")
    except Exception as e:
        print(f"✗ Error: {e}")
    
    print("\n" + "=" * 80)
    print("PART 6: TESTING CONSTRAINTS")
    print("=" * 80)
    
   
    print("\n7. Testing: Trying to close board with incomplete tasks...")
    try:
        board_manager.close_board(json.dumps({"id": "board_1"}))
        print("✗ Board closed with incomplete tasks (shouldn't happen!)")
    except Exception as e:
        print(f"✓ Correctly prevented closing: {e}")
    
   
    print("\n8. Completing all remaining tasks...")
    try:
        board_manager.update_task_status(json.dumps({
            "id": "task_2",
            "status": "COMPLETE"
        }))
        board_manager.update_task_status(json.dumps({
            "id": "task_3",
            "status": "COMPLETE"
        }))
        print("✓ All tasks marked as COMPLETE")
    except Exception as e:
        print(f"✗ Error: {e}")
    
    print("\n9. Now closing the board...")
    try:
        response = board_manager.close_board(json.dumps({"id": "board_1"}))
        print("✓ Board closed successfully!")
        print(json.loads(response)["message"])
    except Exception as e:
        print(f"✗ Error: {e}")
    
    
    print("\n10. Testing: Trying to add task to closed board...")
    try:
        board_manager.add_task(json.dumps({
            "title": "New task",
            "description": "This should fail",
            "user_id": "user_1",
            "board_id": "board_1"
        }))
        print("✗ Task added to closed board (shouldn't happen!)")
    except Exception as e:
        print(f"✓ Correctly prevented adding task: {e}")
    
    
    print("\n11. Testing: Adding task with user not in team...")
    try:
        
        user_manager.create_user(json.dumps({
            "name": "outsider",
            "display_name": "Outside Person"
        }))
        
        board_manager.add_task(json.dumps({
            "title": "Outsider task",
            "description": "Should fail",
            "user_id": "user_5",
            "board_id": "board_2"
        }))
        print("✗ Task assigned to non-team member (shouldn't happen!)")
    except Exception as e:
        print(f"✓ Correctly prevented: {e}")
    
    print("\n" + "=" * 80)
    print("PART 7: CREATING A COMPLETE WORKFLOW")
    print("=" * 80)
    
    
    print("\n12. Creating a complete example workflow for Sprint 2...")
    
    sprint2_tasks = [
        {"title": "Design dashboard layout", "user_id": "user_1"},
        {"title": "Create dashboard API", "user_id": "user_2"},
        {"title": "Implement charts", "user_id": "user_3"},
        {"title": "Add analytics", "user_id": "user_4"}
    ]
    
    for task in sprint2_tasks:
        try:
            board_manager.add_task(json.dumps({
                "title": task["title"],
                "description": f"Work on {task['title'].lower()}",
                "user_id": task["user_id"],
                "board_id": "board_2"
            }))
            print(f"✓ Added: {task['title']}")
        except Exception as e:
            print(f"  {task['title']} might already exist")
    
    print("\n13. Exporting Sprint 2 board...")
    try:
        response = board_manager.export_board(json.dumps({"id": "board_2"}))
        filename = json.loads(response)["out_file"]
        print(f"✓ Sprint 2 exported: out/{filename}")
    except Exception as e:
        print(f"✗ Error: {e}")
    
    print("\n" + "=" * 80)
    print("🎉 ALL TESTS COMPLETED! 🎉")
    print("=" * 80)
    print("\n What You've Built:")
    print("   User Management System")
    print("   Team Management System")
    print("   Project Board System")
    print("   Task Management with Status Tracking")
    print("   Beautiful Board Export Feature")
    print("\n Check these folders:")
    print("  • db/ - All your data (users, teams, boards, tasks)")
    print("  • out/ - Exported board reports")
    print("\n You've built a complete project management system!")
    print("   This is like a mini Trello/Asana!")

if __name__ == "__main__":
    main()