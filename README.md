Team Project Planner
A complete project management system built in Python with user management, team collaboration, and task tracking capabilities.

Overview
This project implements a team-based project planner. It provides a clean API for managing users, teams, project boards, and tasks with full persistence using JSON file storage.

Features

User Management
Create and manage users with unique usernames
Update user profiles
Track user memberships across teams

Team Management
Create teams with designated admins
Add/remove team members (up to 50 per operation)
Prevent admin removal to maintain team ownership
Track all teams a user belongs to

Project Board & Task Management
Create project boards for each team
Add tasks to boards with assignees
Track task status: OPEN → IN_PROGRESS → COMPLETE
Validate that only team members can be assigned tasks
Close boards when all tasks are complete
Export boards to beautifully formatted text reports
Architecture & Design Decisions
File-Based Persistence

I chose JSON file storage for several reasons:

Simplicity: No database setup required, easy to inspect data
Portability: Easy to backup and transfer
Human-readable: JSON files can be manually edited if needed
Sufficient for scale: Works well for small to medium datasets

Object-Oriented Design
Each module extends its base class:

User extends UserBase
Team extends TeamBase
ProjectBoard extends ProjectBoardBase
This provides:

Clear interface contracts
Easy testing and mocking
Future extensibility
Validation & Error Handling
Every API validates inputs and raises descriptive exceptions:

Character limits (names: 64 chars, descriptions: 128 chars)
Uniqueness constraints
Relationship integrity (e.g., users must exist before assignment)
Business rules (e.g., can't remove admins, can't close incomplete boards)


Getting Started
Prerequisites
Python 3.7 or higher
No external dependencies required!


Test User Management:

bash
python test_user.py
Test Team Management:

bash
python test_team.py
Test Complete System:

bash
python test_board.py

Usage Examples
Creating a User
python
from user import User
import json

user_manager = User()
response = user_manager.create_user(json.dumps({
    "name": "joh_laal",
    "display_name": "Joh laal"
}))
# Returns: {"id": "user_1"}
Creating a Team
python
from team import Team
import json

team_manager = Team()
response = team_manager.create_team(json.dumps({
    "name": "Backend Team",
    "description": "Handles all backend services",
    "admin": "user_1"
}))
# Returns: {"id": "team_1"}
Creating a Board and Adding Tasks
python
from project_board import ProjectBoard
import json

board_manager = ProjectBoard()

# Create board
board_response = board_manager.create_board(json.dumps({
    "name": "Sprint 1",
    "description": "First sprint tasks",
    "team_id": "team_1"
}))

# Add task
task_response = board_manager.add_task(json.dumps({
    "title": "Implement login API",
    "description": "Create REST endpoints",
    "user_id": "user_1",
    "board_id": "board_1"
}))

# Update task status
board_manager.update_task_status(json.dumps({
    "id": "task_1",
    "status": "IN_PROGRESS"
}))
Exporting a Board
python
response = board_manager.export_board(json.dumps({
    "id": "board_1"
}))


Future Enhancements
If more time were available, I would add:

* User authentication and authorization
* Soft delete functionality
* Task comments and activity logs
* Search and filter capabilities
* Database migration script (JSON → SQL)


The project includes three test files:

test_user.py - Tests user CRUD operations
test_team.py - Tests team management and membership
test_board.py - Tests complete workflow with boards and tasks
Each test file demonstrates:

 Happy path scenarios
 Error handling and validation
 Business rule enforcement
Performance Considerations
Current approach: Load entire JSON file, modify, save

Date: December 2024
Python Version: 3.7+

