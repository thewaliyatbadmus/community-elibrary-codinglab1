# student.py
#!/usr/bin/env python3
"""
Community E-Library System - Student Interface
Contains all student-related functionality and interface methods
"""

from typing import List
from storage import Resource

class StudentInterface:
    """Student interface functionality for the library system"""
    
    def __init__(self, library, cli_helper):
        self.library = library
        self.cli = cli_helper
    
    def student_interface(self):
        """Handle student interface"""
        while True:
            self.cli.clear_screen()
            self.cli.display_header("Student Access")
            
            if not self.library.current_user:
                print("Are you already registered? (Y/N)")
                registered = input().strip().upper()
                
                if registered == 'Y':
                    if not self.student_login():
                        continue
                elif registered == 'N':
                    print("\n1. Register new account")
                    print("2. Continue as guest")
                    
                    choice = self.cli.get_input("Enter your choice: ", int)
                    
                    if choice == 1:
                        if not self.student_registration():
                            continue
                    elif choice == 2:
                        print("Continuing as guest...")
                        input("Press Enter to continue...")
                    else:
                        print("Invalid choice.")
                        input("Press Enter to continue...")
                        continue
                else:
                    print("Invalid choice.")
                    input("Press Enter to continue...")
                    continue
            
            # Main student menu
            self.student_main_menu()
            break
    
    def student_login(self) -> bool:
        """Handle student login"""
        print("\n--- Student Login ---")
        username = input("Username: ")
        password = input("Password: ")
        
        if self.library.login(username, password):
            if self.library.current_user.role == 'student':
                print(f"Welcome back, {username}!")
                input("Press Enter to continue...")
                return True
            else:
                print("Access denied. Student account required.")
                self.library.logout()
        else:
            print("Invalid credentials.")
        
        input("Press Enter to continue...")
        return False
    
    def student_registration(self) -> bool:
        """Handle student registration"""
        print("\n--- Student Registration ---")
        username = input("Choose a username: ")
        password = input("Choose a password: ")
        email = input("Email (optional): ")
        
        if self.library.register_user(username, password, email):
            print("Registration successful!")
            if self.library.login(username, password):
                print(f"Welcome, {username}!")
                input("Press Enter to continue...")
                return True
        else:
            print("Username already exists.")
        
        input("Press Enter to continue...")
        return False
    
    def student_main_menu(self):
        """Main student menu"""
        while True:
            self.cli.clear_screen()
            self.cli.display_header("Main Library")
            
            if self.library.current_user:
                print(f"Logged in as: {self.library.current_user.username}")
            else:
                print("Browsing as: Guest")
            
            print("\n1. Browse Categories")
            print("2. Search Library")
            print("3. View Favorites")
            print("4. Logout")
            
            choice = self.cli.get_input("\nEnter your choice: ", int)
            
            if choice == 1:
                self.browse_categories()
            elif choice == 2:
                self.search_library()
            elif choice == 3:
                self.view_favorites()
            elif choice == 4:
                self.library.logout()
                break
            else:
                print("Invalid choice.")
                input("Press Enter to continue...")
    
    def browse_categories(self):
        """Browse resources by category"""
        while True:
            self.cli.clear_screen()
            self.cli.display_header("Browse Categories")
            
            for i, category in enumerate(self.library.categories, 1):
                resource_count = len(self.library.get_resources_by_category(category))
                print(f"{i}. {category} ({resource_count} resources)")
            
            print(f"{len(self.library.categories) + 1}. Return to Main Menu")
            
            choice = self.cli.get_input("\nEnter your choice: ", int)
            
            if 1 <= choice <= len(self.library.categories):
                category = self.library.categories[choice - 1]
                self.display_resources(self.library.get_resources_by_category(category), category)
            elif choice == len(self.library.categories) + 1:
                break
            else:
                print("Invalid choice.")
                input("Press Enter to continue...")
    
    def search_library(self):
        """Search for resources"""
        self.cli.clear_screen()
        self.cli.display_header("Search Library")
        
        keyword = input("Enter keyword to search by title, author, or subject: ")
        results = self.library.search_resources(keyword)
        
        if results:
            self.display_resources(results, f"Search Results for '{keyword}'")
        else:
            print(f"No resources found for '{keyword}'")
            input("Press Enter to continue...")
    
    def display_resources(self, resources: List[Resource], title: str):
        """Display a list of resources"""
        while True:
            self.cli.clear_screen()
            self.cli.display_header(title)
            
            if not resources:
                print("No resources available.")
                input("Press Enter to return...")
                break
            
            for i, resource in enumerate(resources, 1):
                print(f"{i}. {resource.title}")
                print(f"   Author: {resource.author}")
                print(f"   Subject: {resource.subject}")
                print(f"   Language: {resource.language}")
                print(f"   Downloads: {resource.download_count} | Views: {resource.view_count}")
                print()
            
            print(f"{len(resources) + 1}. Return to previous menu")
            
            choice = self.cli.get_input("\nSelect a resource: ", int)
            
            if 1 <= choice <= len(resources):
                self.resource_actions(resources[choice - 1])
            elif choice == len(resources) + 1:
                break
            else:
                print("Invalid choice.")
                input("Press Enter to continue...")
    
    def resource_actions(self, resource):
        """Handle actions for a selected resource"""
        while True:
            self.cli.clear_screen()
            self.cli.display_header(f"Resource: {resource.title}")
            
            print(f"Author: {resource.author}")
            print(f"Subject: {resource.subject}")
            print(f"Language: {resource.language}")
            print(f"Category: {resource.category}")
            print(f"Description: {resource.description}")
            print(f"Downloads: {resource.download_count} | Views: {resource.view_count}")
            
            print("\nChoose an action:")
            print("1. View Online")
            print("2. Download File")
            print("3. Add to Favorites")
            print("4. Return to Library")
            
            choice = self.cli.get_input("\nEnter your choice: ", int)
            
            if choice == 1:
                print(self.library.view_resource(resource.id))
                input("Press Enter to continue...")
            elif choice == 2:
                print(self.library.download_resource(resource.id))
                input("Press Enter to continue...")
            elif choice == 3:
                if self.library.current_user:
                    if self.library.add_to_favorites(resource.id):
                        print("Added to favorites!")
                    else:
                        print("Already in favorites or error occurred.")
                else:
                    print("Please login to add favorites.")
                input("Press Enter to continue...")
            elif choice == 4:
                break
            else:
                print("Invalid choice.")
                input("Press Enter to continue...")
    
    def view_favorites(self):
        """View user's favorite resources"""
        if not self.library.current_user:
            print("Please login to view favorites.")
            input("Press Enter to continue...")
            return
        
        favorites = self.library.get_user_favorites()
        self.display_resources(favorites, "Your Favorites")
