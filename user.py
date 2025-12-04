import json
import os
from datetime import datetime

from .user_base import UserBase  


class User(UserBase):
    
    
    def __init__(self):
        """Initialize the User class and create db folder if it doesn't exist"""
        self.db_folder = "db"
        self.users_file = os.path.join(self.db_folder, "users.json")
        self.user_teams_file = os.path.join(self.db_folder, "user_teams.json")
        
        
        if not os.path.exists(self.db_folder):
            os.makedirs(self.db_folder)
        
        self._initialize_files()
    
    def _initialize_files(self):
        """Create empty JSON files if they don't exist"""
        if not os.path.exists(self.users_file):
            with open(self.users_file, 'w') as f:
                json.dump({}, f)
        
        if not os.path.exists(self.user_teams_file):
            with open(self.user_teams_file, 'w') as f:
                json.dump({}, f)
    
    def _load_users(self):
        """Load all users from the JSON file"""
        with open(self.users_file, 'r') as f:
            return json.load(f)
    
    def _save_users(self, users):
        """Save users to the JSON file"""
        with open(self.users_file, 'w') as f:
            json.dump(users, f, indent=2)
    
    def _load_user_teams(self):
        """Load user-team mappings from JSON file"""
        with open(self.user_teams_file, 'r') as f:
            return json.load(f)
    
    def _generate_user_id(self, users):
        """Generate a unique user ID"""
        if not users:
            return "user_1"
        
        # Find the highest number and increment
        max_num = 0
        for user_id in users.keys():
            num = int(user_id.split('_')[1])
            max_num = max(max_num, num)
        
        return f"user_{max_num + 1}"
    
    def create_user(self, request: str) -> str:
        """
        Create a new user
        
        Example request:
        {
          "name": "john_doe",
          "display_name": "John Doe"
        }
        """
        try:
            
            req_data = json.loads(request)
            name = req_data.get("name")
            display_name = req_data.get("display_name")
            
            
            if not name or not display_name:
                raise ValueError("Both name and display_name are required")
            
            if len(name) > 64:
                raise ValueError("Name cannot exceed 64 characters")
            
            if len(display_name) > 64:
                raise ValueError("Display name cannot exceed 64 characters")
            
            
            users = self._load_users()
            
            
            for user_id, user_data in users.items():
                if user_data["name"] == name:
                    raise ValueError(f"User with name '{name}' already exists")
            
            
            user_id = self._generate_user_id(users)
            
            
            user_data = {
                "name": name,
                "display_name": display_name,
                "creation_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            
           
            users[user_id] = user_data
            self._save_users(users)
            
            
            return json.dumps({"id": user_id})
        
        except json.JSONDecodeError:
            raise ValueError("Invalid JSON format in request")
        except Exception as e:
            raise Exception(f"Error creating user: {str(e)}")
    
    def list_users(self) -> str:
        """
        List all users
        
        Returns a JSON array of all users
        """
        users = self._load_users()
        user_list = []
        
        for user_id, user_data in users.items():
            user_list.append({
                "id": user_id,
                "name": user_data["name"],
                "display_name": user_data["display_name"],
                "creation_time": user_data["creation_time"]
            })
        
        return json.dumps(user_list, indent=2)
    
    def describe_user(self, request: str) -> str:
        """
        Get details of a specific user
        
        Example request:
        {
          "id": "user_1"
        }
        """
        try:
            req_data = json.loads(request)
            user_id = req_data.get("id")
            
            if not user_id:
                raise ValueError("User ID is required")
            
            users = self._load_users()
            
            if user_id not in users:
                raise ValueError(f"User with ID '{user_id}' not found")
            
            user_data = users[user_id]
            return json.dumps(user_data, indent=2)
        
        except json.JSONDecodeError:
            raise ValueError("Invalid JSON format in request")
        except Exception as e:
            raise Exception(f"Error describing user: {str(e)}")
    
    def update_user(self, request: str) -> str:
        """
        Update user details (display_name only, name cannot be changed)
        
        Example request:
        {
          "id": "user_1",
          "user": {
            "display_name": "John M. Doe"
          }
        }
        """
        try:
            req_data = json.loads(request)
            user_id = req_data.get("id")
            user_updates = req_data.get("user", {})
            
            if not user_id:
                raise ValueError("User ID is required")
            
            users = self._load_users()
            
            if user_id not in users:
                raise ValueError(f"User with ID '{user_id}' not found")
            
            display_name = user_updates.get("display_name")
            if display_name:
                if len(display_name) > 128:
                    raise ValueError("Display name cannot exceed 128 characters")
                users[user_id]["display_name"] = display_name
            
            if "name" in user_updates:
                raise ValueError("User name cannot be updated")
            
            self._save_users(users)
            
            return json.dumps({"message": "User updated successfully"})
        
        except json.JSONDecodeError:
            raise ValueError("Invalid JSON format in request")
        except Exception as e:
            raise Exception(f"Error updating user: {str(e)}")
    
    def get_user_teams(self, request: str) -> str:
        """
        Get all teams that a user belongs to
        
        Example request:
        {
          "id": "user_1"
        }
        """
        try:
            req_data = json.loads(request)
            user_id = req_data.get("id")
            
            if not user_id:
                raise ValueError("User ID is required")
            
            users = self._load_users()
            if user_id not in users:
                raise ValueError(f"User with ID '{user_id}' not found")
            
            user_teams = self._load_user_teams()
            teams = user_teams.get(user_id, [])
            
            return json.dumps(teams, indent=2)
        
        except json.JSONDecodeError:
            raise ValueError("Invalid JSON format in request")
        except Exception as e:
            raise Exception(f"Error getting user teams: {str(e)}")
    