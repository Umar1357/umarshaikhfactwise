import json
import os
from datetime import datetime
from .team_base import TeamBase


class Team(TeamBase):
    """
    Concrete implementation of TeamBase for managing teams.
    Uses JSON file storage in the db folder.
    """
    
    def __init__(self):
        """Initialize the Team class"""
        self.db_folder = "db"
        self.teams_file = os.path.join(self.db_folder, "teams.json")
        self.team_members_file = os.path.join(self.db_folder, "team_members.json")
        self.users_file = os.path.join(self.db_folder, "users.json")
        self.user_teams_file = os.path.join(self.db_folder, "user_teams.json")
        
        # Create db folder if it doesn't exist
        if not os.path.exists(self.db_folder):
            os.makedirs(self.db_folder)
        
        self._initialize_files()
    
    def _initialize_files(self):
        """Create empty JSON files if they don't exist"""
        if not os.path.exists(self.teams_file):
            with open(self.teams_file, 'w') as f:
                json.dump({}, f)
        
        if not os.path.exists(self.team_members_file):
            with open(self.team_members_file, 'w') as f:
                json.dump({}, f)
        
        if not os.path.exists(self.user_teams_file):
            with open(self.user_teams_file, 'w') as f:
                json.dump({}, f)
    
    def _load_teams(self):
        """Load all teams from JSON file"""
        with open(self.teams_file, 'r') as f:
            return json.load(f)
    
    def _save_teams(self, teams):
        """Save teams to JSON file"""
        with open(self.teams_file, 'w') as f:
            json.dump(teams, f, indent=2)
    
    def _load_team_members(self):
        """Load team members mapping"""
        with open(self.team_members_file, 'r') as f:
            return json.load(f)
    
    def _save_team_members(self, team_members):
        """Save team members mapping"""
        with open(self.team_members_file, 'w') as f:
            json.dump(team_members, f, indent=2)
    
    def _load_users(self):
        """Load users to verify they exist"""
        if not os.path.exists(self.users_file):
            return {}
        with open(self.users_file, 'r') as f:
            return json.load(f)
    
    def _load_user_teams(self):
        """Load user-teams mapping"""
        with open(self.user_teams_file, 'r') as f:
            return json.load(f)
    
    def _save_user_teams(self, user_teams):
        """Save user-teams mapping"""
        with open(self.user_teams_file, 'w') as f:
            json.dump(user_teams, f, indent=2)
    
    def _generate_team_id(self, teams):
        """Generate a unique team ID"""
        if not teams:
            return "team_1"
        
        max_num = 0
        for team_id in teams.keys():
            num = int(team_id.split('_')[1])
            max_num = max(max_num, num)
        
        return f"team_{max_num + 1}"
    
    def create_team(self, request: str) -> str:
        """
        Create a new team
        
        Example request:
        {
          "name": "Backend Team",
          "description": "Handles all backend services",
          "admin": "user_1"
        }
        """
        try:
            req_data = json.loads(request)
            name = req_data.get("name")
            description = req_data.get("description")
            admin = req_data.get("admin")
            
            # Validate IPuts
            if not name:
                raise ValueError("Team name is required")
            
            if not description:
                raise ValueError("Description is required")
            
            if not admin:
                raise ValueError("Admin user ID is required")
            
            if len(name) > 64:
                raise ValueError("Team name cannot exceed 64 characters")
            
            if len(description) > 128:
                raise ValueError("Description cannot exceed 128 characters")
            
            
            users = self._load_users()
            if admin not in users:
                raise ValueError(f"Admin user '{admin}' does not exist")
            
            teams = self._load_teams()
            
            for team_id, team_data in teams.items():
                if team_data["name"] == name:
                    raise ValueError(f"Team with name '{name}' already exists")
            
            team_id = self._generate_team_id(teams)
            
            team_data = {
                "name": name,
                "description": description,
                "creation_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "admin": admin
            }
            
            teams[team_id] = team_data
            self._save_teams(teams)
            
            team_members = self._load_team_members()
            team_members[team_id] = [admin]  
            self._save_team_members(team_members)
            
            user_teams = self._load_user_teams()
            if admin not in user_teams:
                user_teams[admin] = []
            
            user_teams[admin].append({
                "id": team_id,
                "name": name,
                "description": description,
                "creation_time": team_data["creation_time"]
            })
            self._save_user_teams(user_teams)
            
            return json.dumps({"id": team_id})
        
        except json.JSONDecodeError:
            raise ValueError("Invalid JSON format in request")
        except Exception as e:
            raise Exception(f"Error creating team: {str(e)}")
    
    def list_teams(self) -> str:
        """List all teams"""
        teams = self._load_teams()
        team_list = []
        
        for team_id, team_data in teams.items():
            team_list.append({
                "id": team_id,
                "name": team_data["name"],
                "description": team_data["description"],
                "creation_time": team_data["creation_time"],
                "admin": team_data["admin"]
            })
        
        return json.dumps(team_list, indent=2)
    
    def describe_team(self, request: str) -> str:
        """
        Get details of a specific team
        
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
            
            return json.dumps(teams[team_id], indent=2)
        
        except json.JSONDecodeError:
            raise ValueError("Invalid JSON format in request")
        except Exception as e:
            raise Exception(f"Error describing team: {str(e)}")
    
    def update_team(self, request: str) -> str:
        """
        Update team details
        
        Example request:
        {
          "id": "team_1",
          "team": {
            "name": "Updated Backend Team",
            "description": "New description",
            "admin": "user_2"
          }
        }
        """
        try:
            req_data = json.loads(request)
            team_id = req_data.get("id")
            team_updates = req_data.get("team", {})
            
            if not team_id:
                raise ValueError("Team ID is required")
            
            teams = self._load_teams()
            
            if team_id not in teams:
                raise ValueError(f"Team with ID '{team_id}' not found")
            
            if "name" in team_updates:
                new_name = team_updates["name"]
                if len(new_name) > 64:
                    raise ValueError("Team name cannot exceed 64 characters")
                
                for tid, tdata in teams.items():
                    if tid != team_id and tdata["name"] == new_name:
                        raise ValueError(f"Team with name '{new_name}' already exists")
                
                teams[team_id]["name"] = new_name
            
            if "description" in team_updates:
                new_desc = team_updates["description"]
                if len(new_desc) > 128:
                    raise ValueError("Description cannot exceed 128 characters")
                teams[team_id]["description"] = new_desc
            
            if "admin" in team_updates:
                new_admin = team_updates["admin"]
                users = self._load_users()
                if new_admin not in users:
                    raise ValueError(f"Admin user '{new_admin}' does not exist")
                
                team_members = self._load_team_members()
                if new_admin not in team_members.get(team_id, []):
                    team_members[team_id].append(new_admin)
                    self._save_team_members(team_members)
                
                teams[team_id]["admin"] = new_admin
            
            self._save_teams(teams)
            
            return json.dumps({"message": "Team updated successfully"})
        
        except json.JSONDecodeError:
            raise ValueError("Invalid JSON format in request")
        except Exception as e:
            raise Exception(f"Error updating team: {str(e)}")
    
    def add_users_to_team(self, request: str):
        """
        Add users to a team
        
        Example request:
        {
          "id": "team_1",
          "users": ["user_2", "user_3"]
        }
        """
        try:
            req_data = json.loads(request)
            team_id = req_data.get("id")
            user_ids = req_data.get("users", [])
            
            if not team_id:
                raise ValueError("Team ID is required")
            
            if not user_ids:
                raise ValueError("At least one user ID is required")
            
            if len(user_ids) > 50:
                raise ValueError("Cannot add more than 50 users at once")
            
            teams = self._load_teams()
            if team_id not in teams:
                raise ValueError(f"Team with ID '{team_id}' not found")
            
            users = self._load_users()
            for user_id in user_ids:
                if user_id not in users:
                    raise ValueError(f"User '{user_id}' does not exist")
            
            team_members = self._load_team_members()
            if team_id not in team_members:
                team_members[team_id] = []
            
            team_data = teams[team_id]
            user_teams = self._load_user_teams()
            
            for user_id in user_ids:
                if user_id not in team_members[team_id]:
                    team_members[team_id].append(user_id)
                    
                    if user_id not in user_teams:
                        user_teams[user_id] = []
                    
                    team_exists = any(t["id"] == team_id for t in user_teams[user_id])
                    if not team_exists:
                        user_teams[user_id].append({
                            "id": team_id,
                            "name": team_data["name"],
                            "description": team_data["description"],
                            "creation_time": team_data["creation_time"]
                        })
            
            self._save_team_members(team_members)
            self._save_user_teams(user_teams)
            
            return json.dumps({"message": "Users added to team successfully"})
        
        except json.JSONDecodeError:
            raise ValueError("Invalid JSON format in request")
        except Exception as e:
            raise Exception(f"Error adding users to team: {str(e)}")
    
    def remove_users_from_team(self, request: str):
        """
        Remove users from a team
        
        Example request:
        {
          "id": "team_1",
          "users": ["user_2", "user_3"]
        }
        """
        try:
            req_data = json.loads(request)
            team_id = req_data.get("id")
            user_ids = req_data.get("users", [])
            
            if not team_id:
                raise ValueError("Team ID is required")
            
            if not user_ids:
                raise ValueError("At least one user ID is required")
            
            teams = self._load_teams()
            if team_id not in teams:
                raise ValueError(f"Team with ID '{team_id}' not found")
            
            team_members = self._load_team_members()
            if team_id not in team_members:
                team_members[team_id] = []
            
            user_teams = self._load_user_teams()
            
            for user_id in user_ids:
                if user_id in team_members[team_id]:

                    if user_id == teams[team_id]["admin"]:
                        raise ValueError(f"Cannot remove admin user '{user_id}' from team")
                    
                    team_members[team_id].remove(user_id)
                    
                    if user_id in user_teams:
                        user_teams[user_id] = [t for t in user_teams[user_id] if t["id"] != team_id]
            
            self._save_team_members(team_members)
            self._save_user_teams(user_teams)
            
            return json.dumps({"message": "Users removed from team successfully"})
        
        except json.JSONDecodeError:
            raise ValueError("Invalid JSON format in request")
        except Exception as e:
            raise Exception(f"Error removing users from team: {str(e)}")
    
    def list_team_users(self, request: str):
        """
        List all users in a team
        
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
            
            team_members = self._load_team_members()
            member_ids = team_members.get(team_id, [])
            
            users = self._load_users()
            user_list = []
            
            for user_id in member_ids:
                if user_id in users:
                    user_data = users[user_id]
                    user_list.append({
                        "id": user_id,
                        "name": user_data["name"],
                        "display_name": user_data["display_name"]
                    })
            
            return json.dumps(user_list, indent=2)
        
        except json.JSONDecodeError:
            raise ValueError("Invalid JSON format in request")
        except Exception as e:
            raise Exception(f"Error listing team users: {str(e)}")