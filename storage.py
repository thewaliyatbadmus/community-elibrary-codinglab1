#!/usr/bin/env python3
"""
Community E-Library System - Storage and Data Models
Contains User, Resource classes and ELibrary storage management
"""

import json
import os
import datetime
from typing import Dict, List, Optional
import hashlib
import subprocess
import platform
import shutil
import webbrowser
from urllib.parse import urlparse

class User:
    """User class for managing library users"""
    
    def __init__(self, username: str, password: str, email: str = "", role: str = "student"):
        self.username = username
        self.password = self._hash_password(password)
        self.email = email
        self.role = role
        self.favorites = []
        self.reading_history = []
        self.created_at = datetime.datetime.now().isoformat()
    
    def _hash_password(self, password: str) -> str:
        """Hash password using SHA256"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def verify_password(self, password: str) -> bool:
        """Verify password against stored hash"""
        return self.password == self._hash_password(password)
    
    def to_dict(self):
        """Convert user to dictionary for JSON serialization"""
        return {
            'username': self.username,
            'password': self.password,
            'email': self.email,
            'role': self.role,
            'favorites': self.favorites,
            'reading_history': self.reading_history,
            'created_at': self.created_at
        }
    
    @classmethod
    def from_dict(cls, data):
        """Create user from dictionary"""
        user = cls.__new__(cls)
        user.username = data['username']
        user.password = data['password']
        user.email = data.get('email', '')
        user.role = data.get('role', 'student')
        user.favorites = data.get('favorites', [])
        user.reading_history = data.get('reading_history', [])
        user.created_at = data.get('created_at', datetime.datetime.now().isoformat())
        return user

class Resource:
    """Resource class for managing library resources"""
    
    def __init__(self, title: str, author: str, subject: str, language: str, 
                 file_path: str, category: str = "Core Subjects", description: str = ""):
        self.id = self._generate_id()
        self.title = title
        self.author = author
        self.subject = subject
        self.language = language
        self.file_path = file_path
        self.category = category
        self.description = description
        self.download_count = 0
        self.view_count = 0
        self.added_date = datetime.datetime.now().isoformat()
    
    def _generate_id(self) -> str:
        """Generate unique ID for resource"""
        return hashlib.md5(f"{datetime.datetime.now().isoformat()}".encode()).hexdigest()[:8]
    
    def to_dict(self):
        """Convert resource to dictionary for JSON serialization"""
        return {
            'id': self.id,
            'title': self.title,
            'author': self.author,
            'subject': self.subject,
            'language': self.language,
            'file_path': self.file_path,
            'category': self.category,
            'description': self.description,
            'download_count': self.download_count,
            'view_count': self.view_count,
            'added_date': self.added_date
        }
    
    @classmethod
    def from_dict(cls, data):
        """Create resource from dictionary"""
        resource = cls.__new__(cls)
        resource.id = data['id']
        resource.title = data['title']
        resource.author = data['author']
        resource.subject = data['subject']
        resource.language = data['language']
        resource.file_path = data['file_path']
        resource.category = data.get('category', 'Core Subjects')
        resource.description = data.get('description', '')
        resource.download_count = data.get('download_count', 0)
        resource.view_count = data.get('view_count', 0)
        resource.added_date = data.get('added_date', datetime.datetime.now().isoformat())
        return resource

class ELibrary:
    """Main library class for managing users, resources and data persistence"""
    
    def __init__(self):
        self.users = {}
        self.resources = {}
        self.current_user = None
        self.data_file = 'library_data.json'
        self.categories = [
            "Core Subjects",
            "Local Storybooks", 
            "Study Skills",
            "Exam Guides"
        ]
        self.load_data()
        self._create_default_admin()
    
    def _create_default_admin(self):
        """Create default admin user if none exists"""
        admin_exists = any(user.role == 'admin' for user in self.users.values())
        if not admin_exists:
            admin = User("admin", "admin123", "admin@library.com", "admin")
            self.users["admin"] = admin
            self.save_data()
            print("Default admin created - Username: admin, Password: admin123")
    
    def load_data(self):
        """Load data from JSON file"""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r') as f:
                    data = json.load(f)
                    
                # Load users
                for username, user_data in data.get('users', {}).items():
                    self.users[username] = User.from_dict(user_data)
                
                # Load resources
                for resource_id, resource_data in data.get('resources', {}).items():
                    self.resources[resource_id] = Resource.from_dict(resource_data)
                    
            except (json.JSONDecodeError, KeyError) as e:
                print(f"Error loading data: {e}")
                print("Starting with empty library...")
    
    def save_data(self):
        """Save data to JSON file"""
        data = {
            'users': {username: user.to_dict() for username, user in self.users.items()},
            'resources': {resource_id: resource.to_dict() for resource_id, resource in self.resources.items()}
        }
        
        try:
            with open(self.data_file, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            print(f"Error saving data: {e}")
    
    def register_user(self, username: str, password: str, email: str = "") -> bool:
        """Register a new user"""
        if username in self.users:
            return False
        
        self.users[username] = User(username, password, email)
        self.save_data()
        return True
    
    def login(self, username: str, password: str) -> bool:
        """Authenticate user login"""
        if username in self.users and self.users[username].verify_password(password):
            self.current_user = self.users[username]
            return True
        return False
    
    def logout(self):
        """Logout current user"""
        self.current_user = None
    
    def add_resource(self, title: str, author: str, subject: str, language: str, 
                    file_path: str, category: str = "Core Subjects", description: str = "") -> str:
        """Add a new resource to the library"""
        resource = Resource(title, author, subject, language, file_path, category, description)
        self.resources[resource.id] = resource
        self.save_data()
        return resource.id
    
    def search_resources(self, keyword: str) -> List[Resource]:
        """Search resources by keyword"""
        results = []
        keyword_lower = keyword.lower()
        
        for resource in self.resources.values():
            if (keyword_lower in resource.title.lower() or 
                keyword_lower in resource.author.lower() or 
                keyword_lower in resource.subject.lower() or
                keyword_lower in resource.language.lower()):
                results.append(resource)
        
        return results
    
    def get_resources_by_category(self, category: str) -> List[Resource]:
        """Get all resources in a specific category"""
        return [resource for resource in self.resources.values() 
                if resource.category == category]
    
    def view_resource(self, resource_id: str):
        """Open a resource for viewing"""
        if resource_id in self.resources:
            resource = self.resources[resource_id]
            resource.view_count += 1
            
            if self.current_user:
                if resource_id not in self.current_user.reading_history:
                    self.current_user.reading_history.append(resource_id)
            
            self.save_data()
            
            # Try to open the file/URL
            file_path = resource.file_path
            
            # Check if it's a URL
            if self._is_url(file_path):
                try:
                    webbrowser.open(file_path)
                    return f"Opening '{resource.title}' in your web browser..."
                except Exception as e:
                    return f"Error opening URL: {str(e)}"
            
            # Check if it's a local file
            elif os.path.exists(file_path):
                try:
                    self._open_file(file_path)
                    return f"Opening '{resource.title}' by {resource.author}..."
                except Exception as e:
                    return f"Error opening file: {str(e)}"
            else:
                return f"File not found: {file_path}\nNote: This might be a placeholder path. Please check with the administrator."
        
        return "Resource not found"
    
    def download_resource(self, resource_id: str):
        """Download a resource to local downloads folder"""
        if resource_id in self.resources:
            resource = self.resources[resource_id]
            resource.download_count += 1
            
            if self.current_user:
                if resource_id not in self.current_user.reading_history:
                    self.current_user.reading_history.append(resource_id)
            
            self.save_data()
            
            file_path = resource.file_path
            
            # Create downloads directory if it doesn't exist
            downloads_dir = os.path.join(os.getcwd(), "downloads")
            if not os.path.exists(downloads_dir):
                os.makedirs(downloads_dir)
            
            # If it's a URL, try to download it
            if self._is_url(file_path):
                try:
                    import urllib.request
                    
                    # Get filename from URL or use title
                    filename = self._get_filename_from_url(file_path, resource.title)
                    download_path = os.path.join(downloads_dir, filename)
                    
                    print(f"Downloading from {file_path}...")
                    urllib.request.urlretrieve(file_path, download_path)
                    
                    return f"Downloaded '{resource.title}' to: {download_path}"
                    
                except Exception as e:
                    return f"Error downloading from URL: {str(e)}"
            
            # If it's a local file, copy it to downloads
            elif os.path.exists(file_path):
                try:
                    filename = os.path.basename(file_path)
                    if not filename:
                        filename = f"{resource.title.replace(' ', '_')}.pdf"
                    
                    download_path = os.path.join(downloads_dir, filename)
                    shutil.copy2(file_path, download_path)
                    
                    return f"Downloaded '{resource.title}' to: {download_path}"
                    
                except Exception as e:
                    return f"Error copying file: {str(e)}"
            else:
                return f"File not found: {file_path}\nNote: This might be a placeholder path. Please check with the administrator."
        
        return "Resource not found"
    
    def add_to_favorites(self, resource_id: str) -> bool:
        """Add resource to user's favorites"""
        if self.current_user and resource_id in self.resources:
            if resource_id not in self.current_user.favorites:
                self.current_user.favorites.append(resource_id)
                self.save_data()
                return True
        return False
    
    def get_user_favorites(self) -> List[Resource]:
        """Get current user's favorite resources"""
        if not self.current_user:
            return []
        
        return [self.resources[resource_id] for resource_id in self.current_user.favorites 
                if resource_id in self.resources]
    
    def get_usage_report(self) -> Dict:
        """Generate usage report for admin"""
        total_resources = len(self.resources)
        total_users = len([user for user in self.users.values() if user.role == 'student'])
        
        # Most downloaded resources
        most_downloaded = sorted(self.resources.values(), 
                               key=lambda x: x.download_count, reverse=True)[:5]
        
        # Most viewed resources
        most_viewed = sorted(self.resources.values(), 
                           key=lambda x: x.view_count, reverse=True)[:5]
        
        return {
            'total_resources': total_resources,
            'total_users': total_users,
            'most_downloaded': most_downloaded,
            'most_viewed': most_viewed
        }
    
    def _is_url(self, path: str) -> bool:
        """Check if a path is a URL"""
        try:
            result = urlparse(path)
            return all([result.scheme, result.netloc])
        except:
            return False
    
    def _open_file(self, file_path: str):
        """Open a file with the default system application"""
        system = platform.system()
        
        if system == "Windows":
            os.startfile(file_path)
        elif system == "Darwin":  # macOS
            subprocess.run(["open", file_path])
        else:  # Linux and other Unix-like systems
            subprocess.run(["xdg-open", file_path])
    
    def _get_filename_from_url(self, url: str, title: str) -> str:
        """Extract filename from URL or create one from title"""
        try:
            parsed = urlparse(url)
            filename = os.path.basename(parsed.path)
            if filename and '.' in filename:
                return filename
        except:
            pass
        
        # If no filename found, create one from title
        safe_title = "".join(c for c in title if c.isalnum() or c in (' ', '-', '_')).rstrip()
        return f"{safe_title.replace(' ', '_')}.pdf"