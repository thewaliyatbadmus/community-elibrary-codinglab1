# admin.py
#!/usr/bin/env python3
"""
Community E-Library System - Admin Interface
Contains all admin-related functionality and interface methods
"""

from storage import User

class AdminInterface:
    """Admin interface functionality for the library system"""
    
    def __init__(self, library, cli_helper):
        self.library = library
        self.cli = cli_helper
    
    def admin_interface(self):
        """Handle admin interface"""
        self.cli.clear_screen()
        self.cli.display_header("Admin Login")
        
        username = input("Username: ")
        password = input("Password: ")
        
        if self.library.login(username, password):
            if self.library.current_user.role == 'admin':
                print(f"Welcome, Admin {username}!")
                input("Press Enter to continue...")
                self.admin_dashboard()
            else:
                print("Access denied. Admin account required.")
                self.library.logout()
                input("Press Enter to continue...")
        else:
            print("Invalid admin credentials.")
            input("Press Enter to continue...")
    
    def admin_dashboard(self):
        """Main admin dashboard"""
        while True:
            self.cli.clear_screen()
            self.cli.display_header("Admin Dashboard")
            
            print(f"Logged in as: {self.library.current_user.username}")
            print("\n1. Add New Resource")
            print("2. Edit Existing Resource")
            print("3. Manage Users")
            print("4. View Usage Report")
            print("5. Logout")
            
            choice = self.cli.get_input("\nEnter your choice: ", int)
            
            if choice == 1:
                self.add_new_resource()
            elif choice == 2:
                self.edit_resource()
            elif choice == 3:
                self.manage_users()
            elif choice == 4:
                self.view_usage_report()
            elif choice == 5:
                self.library.logout()
                break
            else:
                print("Invalid choice.")
                input("Press Enter to continue...")
    
    def add_new_resource(self):
        """Add a new resource"""
        self.cli.clear_screen()
        self.cli.display_header("Add New Resource")
        
        title = input("Enter Title: ")
        author = input("Enter Author: ")
        subject = input("Enter Subject: ")
        language = input("Enter Language: ")
        file_path = input("Enter File Path/URL: ")
        description = input("Enter Description (optional): ")
        
        print("\nSelect Category:")
        for i, category in enumerate(self.library.categories, 1):
            print(f"{i}. {category}")
        
        cat_choice = self.cli.get_input("Enter category number: ", int)
        
        if 1 <= cat_choice <= len(self.library.categories):
            category = self.library.categories[cat_choice - 1]
            
            resource_id = self.library.add_resource(title, author, subject, language, 
                                                  file_path, category, description)
            print(f"\nResource added successfully! ID: {resource_id}")
        else:
            print("Invalid category selection.")
        
        input("Press Enter to continue...")
    
    def edit_resource(self):
        """Edit an existing resource"""
        self.cli.clear_screen()
        self.cli.display_header("Edit Existing Resource")
        
        if not self.library.resources:
            print("No resources available to edit.")
            input("Press Enter to continue...")
            return
        
        resources = list(self.library.resources.values())
        for i, resource in enumerate(resources, 1):
            print(f"{i}. {resource.title} by {resource.author}")
        
        choice = self.cli.get_input(f"\nSelect resource to edit (1-{len(resources)}): ", int)
        
        if 1 <= choice <= len(resources):
            resource = resources[choice - 1]
            
            print(f"\nEditing: {resource.title}")
            print("Press Enter to keep current value")
            
            new_title = input(f"Title [{resource.title}]: ") or resource.title
            new_author = input(f"Author [{resource.author}]: ") or resource.author
            new_subject = input(f"Subject [{resource.subject}]: ") or resource.subject
            new_language = input(f"Language [{resource.language}]: ") or resource.language
            new_file_path = input(f"File Path [{resource.file_path}]: ") or resource.file_path
            new_description = input(f"Description [{resource.description}]: ") or resource.description
            
            # Update resource
            resource.title = new_title
            resource.author = new_author
            resource.subject = new_subject
            resource.language = new_language
            resource.file_path = new_file_path
            resource.description = new_description
            
            self.library.save_data()
            print("Resource updated successfully!")
        else:
            print("Invalid selection.")
        
        input("Press Enter to continue...")
    
    def manage_users(self):
        """Manage users"""
        while True:
            self.cli.clear_screen()
            self.cli.display_header("Manage Users")
            
            print("1. View All Users")
            print("2. Add New Admin")
            print("3. Remove User")
            print("4. Return to Dashboard")
            
            choice = self.cli.get_input("\nEnter your choice: ", int)
            
            if choice == 1:
                self.view_all_users()
            elif choice == 2:
                self.add_new_admin()
            elif choice == 3:
                self.remove_user()
            elif choice == 4:
                break
            else:
                print("Invalid choice.")
                input("Press Enter to continue...")
    
    def view_all_users(self):
        """View all registered users"""
        self.cli.clear_screen()
        self.cli.display_header("All Users")
        
        students = [user for user in self.library.users.values() if user.role == 'student']
        admins = [user for user in self.library.users.values() if user.role == 'admin']
        
        print(f"Total Students: {len(students)}")
        print(f"Total Admins: {len(admins)}")
        print("\n--- Students ---")
        
        for user in students:
            favorites_count = len(user.favorites)
            history_count = len(user.reading_history)
            print(f"Username: {user.username}")
            print(f"Email: {user.email}")
            print(f"Favorites: {favorites_count} | Reading History: {history_count}")
            print(f"Joined: {user.created_at[:10]}")
            print("-" * 30)
        
        print("\n--- Admins ---")
        for user in admins:
            print(f"Username: {user.username}")
            print(f"Email: {user.email}")
            print("-" * 30)
        
        input("Press Enter to continue...")
    
    def add_new_admin(self):
        """Add a new admin user"""
        self.cli.clear_screen()
        self.cli.display_header("Add New Admin")
        
        username = input("Enter admin username: ")
        password = input("Enter admin password: ")
        email = input("Enter admin email: ")
        
        if username not in self.library.users:
            admin = User(username, password, email, "admin")
            self.library.users[username] = admin
            self.library.save_data()
            print("Admin user created successfully!")
        else:
            print("Username already exists.")
        
        input("Press Enter to continue...")
    
    def remove_user(self):
        """Remove a user"""
        self.cli.clear_screen()
        self.cli.display_header("Remove User")
        
        username = input("Enter username to remove: ")
        
        if username in self.library.users:
            if username == self.library.current_user.username:
                print("Cannot remove currently logged in admin.")
            else:
                del self.library.users[username]
                self.library.save_data()
                print(f"User '{username}' removed successfully!")
        else:
            print("User not found.")
        
        input("Press Enter to continue...")
    
    def view_usage_report(self):
        """View usage statistics"""
        self.cli.clear_screen()
        self.cli.display_header("Usage Report")
        
        report = self.library.get_usage_report()
        
        print(f"Total Resources: {report['total_resources']}")
        print(f"Total Students: {report['total_users']}")
        
        print("\n--- Most Downloaded Resources ---")
        for i, resource in enumerate(report['most_downloaded'], 1):
            print(f"{i}. {resource.title} - {resource.download_count} downloads")
        
        print("\n--- Most Viewed Resources ---")
        for i, resource in enumerate(report['most_viewed'], 1):
            print(f"{i}. {resource.title} - {resource.view_count} views")
        
        input("Press Enter to continue...")