import json
import os
from datetime import datetime
from .project_board_base import ProjectBoardBase


class ProjectBoard(ProjectBoardBase):
    """
    Concrete implementation of ProjectBoardBase for managing boards and tasks.
    Uses JSON file storage in the db folder.
    """
    
    def __init__(self):
        """Initialize the ProjectBoard class"""
        self.db_folder = "db"
        self.out_folder = "out"
        self.boards_file = os.path.join(self.db_folder, "boards.json")
        self.tasks_file = os.path.join(self.db_folder, "tasks.json")
        self.teams_file = os.path.join(self.db_folder, "teams.json")
        self.users_file = os.path.join(self.db_folder, "users.json")
        self.team_members_file = os.path.join(self.db_folder, "team_members.json")
        
        # Create folders if they don't exist
        if not os.path.exists(self.db_folder):
            os.makedirs(self.db_folder)
        if not os.path.exists(self.out_folder):
            os.makedirs(self.out_folder)
        
        self._initialize_files()
    
    def _initialize_files(self):
        """Create empty JSON files if they don't exist"""
        if not os.path.exists(self.boards_file):
            with open(self.boards_file, 'w') as f:
                json.dump({}, f)
        
        if not os.path.exists(self.tasks_file):
            with open(self.tasks_file, 'w') as f:
                json.dump({}, f)
    
    def _load_boards(self):
        """Load all boards from JSON file"""
        with open(self.boards_file, 'r') as f:
            return json.load(f)
    
    def _save_boards(self, boards):
        """Save boards to JSON file"""
        with open(self.boards_file, 'w') as f:
            json.dump(boards, f, indent=2)
    
    def _load_tasks(self):
        """Load all tasks from JSON file"""
        with open(self.tasks_file, 'r') as f:
            return json.load(f)
    
    def _save_tasks(self, tasks):
        """Save tasks to JSON file"""
        with open(self.tasks_file, 'w') as f:
            json.dump(tasks, f, indent=2)
    
    def _load_teams(self):
        """Load teams to verify they exist"""
        if not os.path.exists(self.teams_file):
            return {}
        with open(self.teams_file, 'r') as f:
            return json.load(f)
    
    def _load_users(self):
        """Load users to verify they exist"""
        if not os.path.exists(self.users_file):
            return {}
        with open(self.users_file, 'r') as f:
            return json.load(f)
    
    def _load_team_members(self):
        """Load team members"""
        if not os.path.exists(self.team_members_file):
            return {}
        with open(self.team_members_file, 'r') as f:
            return json.load(f)
    
    def _generate_board_id(self, boards):
        """Generate a unique board ID"""
        if not boards:
            return "board_1"
        
        max_num = 0
        for board_id in boards.keys():
            num = int(board_id.split('_')[1])
            max_num = max(max_num, num)
        
        return f"board_{max_num + 1}"
    
    def _generate_task_id(self, tasks):
        """Generate a unique task ID"""
        if not tasks:
            return "task_1"
        
        max_num = 0
        for task_id in tasks.keys():
            num = int(task_id.split('_')[1])
            max_num = max(max_num, num)
        
        return f"task_{max_num + 1}"
    
    def create_board(self, request: str):
        """
        Create a new project board for a team
        
        Example request:
        {
            "name": "Sprint 1",
            "description": "First sprint tasks",
            "team_id": "team_1"
        }
        """
        try:
            req_data = json.loads(request)
            name = req_data.get("name")
            description = req_data.get("description")
            team_id = req_data.get("team_id")
            
            if not name:
                raise ValueError("Board name is required")
            
            if not description:
                raise ValueError("Description is required")
            
            if not team_id:
                raise ValueError("Team ID is required")
            
            if len(name) > 64:
                raise ValueError("Board name cannot exceed 64 characters")
            
            if len(description) > 128:
                raise ValueError("Description cannot exceed 128 characters")
            
            teams = self._load_teams()
            if team_id not in teams:
                raise ValueError(f"Team with ID '{team_id}' does not exist")
            
            boards = self._load_boards()
            
            for board_id, board_data in boards.items():
                if board_data["team_id"] == team_id and board_data["name"] == name:
                    raise ValueError(f"Board with name '{name}' already exists for this team")
            
            board_id = self._generate_board_id(boards)
            
            board_data = {
                "name": name,
                "description": description,
                "team_id": team_id,
                "creation_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "status": "OPEN",
                "end_time": None
            }
            
            boards[board_id] = board_data
            self._save_boards(boards)
            
            return json.dumps({"id": board_id})
        
        except json.JSONDecodeError:
            raise ValueError("Invalid JSON format in request")
        except Exception as e:
            raise Exception(f"Error creating board: {str(e)}")
    
    def close_board(self, request: str) -> str:
        """
        Close a board (only if all tasks are COMPLETE)
        
        Example request:
        {
          "id": "board_1"
        }
        """
        try:
            req_data = json.loads(request)
            board_id = req_data.get("id")
            
            if not board_id:
                raise ValueError("Board ID is required")
            
            boards = self._load_boards()
            
            if board_id not in boards:
                raise ValueError(f"Board with ID '{board_id}' not found")
            
            tasks = self._load_tasks()
            for task_id, task_data in tasks.items():
                if task_data["board_id"] == board_id:
                    if task_data["status"] != "COMPLETE":
                        raise ValueError(f"Cannot close board. Task '{task_data['title']}' is not COMPLETE")
            
            boards[board_id]["status"] = "CLOSED"
            boards[board_id]["end_time"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self._save_boards(boards)
            
            return json.dumps({"message": "Board closed successfully"})
        
        except json.JSONDecodeError:
            raise ValueError("Invalid JSON format in request")
        except Exception as e:
            raise Exception(f"Error closing board: {str(e)}")
    
    def add_task(self, request: str) -> str:
        """
        Add a task to a board
        
        Example request:
        {
            "title": "Implement login API",
            "description": "Create REST API for user authentication",
            "user_id": "user_1",
            "board_id": "board_1"
        }
        """
        try:
            req_data = json.loads(request)
            title = req_data.get("title")
            description = req_data.get("description")
            user_id = req_data.get("user_id")
            board_id = req_data.get("board_id")
            
            if not title:
                raise ValueError("Task title is required")
            
            if not description:
                raise ValueError("Description is required")
            
            if not user_id:
                raise ValueError("User ID is required")
            
            if not board_id:
                raise ValueError("Board ID is required")
            
            if len(title) > 64:
                raise ValueError("Task title cannot exceed 64 characters")
            
            if len(description) > 128:
                raise ValueError("Description cannot exceed 128 characters")
            
            boards = self._load_boards()
            if board_id not in boards:
                raise ValueError(f"Board with ID '{board_id}' does not exist")
            
            if boards[board_id]["status"] != "OPEN":
                raise ValueError("Can only add tasks to OPEN boards")
            
            users = self._load_users()
            if user_id not in users:
                raise ValueError(f"User with ID '{user_id}' does not exist")
            
            team_id = boards[board_id]["team_id"]
            team_members = self._load_team_members()
            if team_id not in team_members or user_id not in team_members[team_id]:
                raise ValueError(f"User '{user_id}' is not a member of the team that owns this board")
            
            tasks = self._load_tasks()
            
            for task_id, task_data in tasks.items():
                if task_data["board_id"] == board_id and task_data["title"] == title:
                    raise ValueError(f"Task with title '{title}' already exists in this board")
            
            task_id = self._generate_task_id(tasks)
            
            task_data = {
                "title": title,
                "description": description,
                "user_id": user_id,
                "board_id": board_id,
                "creation_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "status": "OPEN"
            }
            
            
            tasks[task_id] = task_data
            self._save_tasks(tasks)
            
            return json.dumps({"id": task_id})
        
        except json.JSONDecodeError:
            raise ValueError("Invalid JSON format in request")
        except Exception as e:
            raise Exception(f"Error adding task: {str(e)}")
    
    def update_task_status(self, request: str):
        """
        Update the status of a task
        
        Example request:
        {
            "id": "task_1",
            "status": "IN_PROGRESS"
        }
        """
        try:
            req_data = json.loads(request)
            task_id = req_data.get("id")
            new_status = req_data.get("status")
            
            if not task_id:
                raise ValueError("Task ID is required")
            
            if not new_status:
                raise ValueError("Status is required")
            
        
            valid_statuses = ["OPEN", "IN_PROGRESS", "COMPLETE"]
            if new_status not in valid_statuses:
                raise ValueError(f"Status must be one of: {', '.join(valid_statuses)}")
            
            tasks = self._load_tasks()
            
            if task_id not in tasks:
                raise ValueError(f"Task with ID '{task_id}' not found")
            
           
            tasks[task_id]["status"] = new_status
            self._save_tasks(tasks)
            
            return json.dumps({"message": "Task status updated successfully"})
        
        except json.JSONDecodeError:
            raise ValueError("Invalid JSON format in request")
        except Exception as e:
            raise Exception(f"Error updating task status: {str(e)}")
    
    def list_boards(self, request: str) -> str:
        """
        List all boards for a team
        
        Example request:
        {
          "id": "team_1"
        }
        """
        try:
            req_data = json.loads(request)
            team_id = req_data.get("id")
            
            if not team_id:
                raise ValueError("Team ID is required")
            
          
            teams = self._load_teams()
            if team_id not in teams:
                raise ValueError(f"Team with ID '{team_id}' not found")
            
            
            boards = self._load_boards()
            board_list = []
            
            for board_id, board_data in boards.items():
                if board_data["team_id"] == team_id:
                    board_list.append({
                        "id": board_id,
                        "name": board_data["name"],
                        "status": board_data["status"]
                    })
            
            return json.dumps(board_list, indent=2)
        
        except json.JSONDecodeError:
            raise ValueError("Invalid JSON format in request")
        except Exception as e:
            raise Exception(f"Error listing boards: {str(e)}")
    
    def export_board(self, request: str) -> str:
        """
        Export a board to a beautiful text file in the out folder
        
        Example request:
        {
          "id": "board_1"
        }
        """
        try:
            req_data = json.loads(request)
            board_id = req_data.get("id")
            
            if not board_id:
                raise ValueError("Board ID is required")
            
            boards = self._load_boards()
            
            if board_id not in boards:
                raise ValueError(f"Board with ID '{board_id}' not found")
            
            board_data = boards[board_id]
            
          
            teams = self._load_teams()
            team_data = teams.get(board_data["team_id"], {})
            
            
            tasks = self._load_tasks()
            board_tasks = []
            for task_id, task_data in tasks.items():
                if task_data["board_id"] == board_id:
                    board_tasks.append((task_id, task_data))
            
            
            users = self._load_users()
            
            
            output = []
            output.append("=" * 80)
            output.append(f"PROJECT BOARD: {board_data['name']}")
            output.append("=" * 80)
            output.append(f"Team: {team_data.get('name', 'Unknown')}")
            output.append(f"Description: {board_data['description']}")
            output.append(f"Status: {board_data['status']}")
            output.append(f"Created: {board_data['creation_time']}")
            if board_data['end_time']:
                output.append(f"Closed: {board_data['end_time']}")
            output.append("=" * 80)
            output.append("")
            
            # Group tasks 
            status_groups = {
                "OPEN": [],
                "IN_PROGRESS": [],
                "COMPLETE": []
            }
            
            for task_id, task_data in board_tasks:
                status_groups[task_data["status"]].append((task_id, task_data))
            
            # Display tasks
            for status in ["OPEN", "IN_PROGRESS", "COMPLETE"]:
                tasks_in_status = status_groups[status]
                
                output.append("")
                output.append(f"{'▓' * 80}")
                output.append(f"  {status} ({len(tasks_in_status)} tasks)")
                output.append(f"{'▓' * 80}")
                output.append("")
                
                if not tasks_in_status:
                    output.append("  No tasks in this status")
                    output.append("")
                else:
                    for task_id, task_data in tasks_in_status:
                        user_data = users.get(task_data["user_id"], {})
                        user_name = user_data.get("display_name", "Unknown User")
                        
                        output.append(f"  [{task_id}] {task_data['title']}")
                        output.append(f"  {'─' * 76}")
                        output.append(f"  Description: {task_data['description']}")
                        output.append(f"  Assigned to: {user_name} ({task_data['user_id']})")
                        output.append(f"  Created: {task_data['creation_time']}")
                        output.append("")
            
            output.append("=" * 80)
            output.append(f"SUMMARY")
            output.append("=" * 80)
            output.append(f"Total Tasks: {len(board_tasks)}")
            output.append(f"  • Open: {len(status_groups['OPEN'])}")
            output.append(f"  • In Progress: {len(status_groups['IN_PROGRESS'])}")
            output.append(f"  • Complete: {len(status_groups['COMPLETE'])}")
            
            completion_rate = 0
            if board_tasks:
                completion_rate = (len(status_groups['COMPLETE']) / len(board_tasks)) * 100
            output.append(f"  • Completion Rate: {completion_rate:.1f}%")
            output.append("=" * 80)
            
            safe_name = board_data['name'].replace(' ', '_').replace('/', '_')
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{safe_name}_{board_id}_{timestamp}.txt"
            filepath = os.path.join(self.out_folder, filename)
            
            with open(filepath, 'w', encoding="utf-8") as f:
                f.write('\n'.join(output))
            
            return json.dumps({"out_file": filename})
        
        except json.JSONDecodeError:
            raise ValueError("Invalid JSON format in request")
        except Exception as e:
            raise Exception(f"Error exporting board: {str(e)}")