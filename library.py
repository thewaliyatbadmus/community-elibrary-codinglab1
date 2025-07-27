# =====================================================================
# COMPLETE LIBRARY MANAGEMENT SYSTEM - ALL TEAM MODULES INTEGRATED
# =====================================================================

# ============== LEA'S MODULE: storage.py ==============
import json
import os
from typing import List, Dict, Optional
from datetime import datetime

class StorageManager:
    """
    Lea's Storage System - Handles all file operations and data persistence
    """
    
    def __init__(self, students_file="students.json", books_file="books.json", 
                 logs_file="usage_logs.json"):
        self.students_file = students_file
        self.books_file = books_file
        self.logs_file = logs_file
        self.initialize_files()
    
    def initialize_files(self):
        """Initialize data files with sample data if they don't exist"""
        # Initialize books file
        if not os.path.exists(self.books_file):
            sample_books = [
                {
                    "book_id": 1,
                    "title": "Python Programming",
                    "author": "John Smith",
                    "category": "Programming",
                    "total_copies": 3,
                    "available_copies": 3,
                    "borrowed_by": []
                },
                {
                    "book_id": 2,
                    "title": "Data Structures",
                    "author": "Jane Doe",
                    "category": "Computer Science",
                    "total_copies": 2,
                    "available_copies": 2,
                    "borrowed_by": []
                },
                {
                    "book_id": 3,
                    "title": "Web Development",
                    "author": "Mike Johnson",
                    "category": "Programming",
                    "total_copies": 2,
                    "available_copies": 1,
                    "borrowed_by": ["student1"]
                },
                {
                    "book_id": 4,
                    "title": "Machine Learning",
                    "author": "Sarah Wilson",
                    "category": "AI/ML",
                    "total_copies": 1,
                    "available_copies": 1,
                    "borrowed_by": []
                },
                {
                    "book_id": 5,
                    "title": "Database Systems",
                    "author": "Robert Brown",
                    "category": "Computer Science",
                    "total_copies": 2,
                    "available_copies": 2,
                    "borrowed_by": []
                }
            ]
            self.save_json(self.books_file, {"books": sample_books, "next_book_id": 6})
        
        # Initialize students file
        if not os.path.exists(self.students_file):
            sample_students = [
                {
                    "student_id": "admin",
                    "name": "System Administrator",
                    "email": "admin@library.com",
                    "user_type": "admin",
                    "borrowed_books": [],
                    "favorites": [],
                    "registration_date": datetime.now().isoformat()
                }
            ]
            self.save_json(self.students_file, {"students": sample_students})
        
        # Initialize logs file
        if not os.path.exists(self.logs_file):
            self.save_json(self.logs_file, {"logs": []})
    
    def save_json(self, filename: str, data: Dict) -> bool:
        """Save data to JSON file"""
        try:
            with open(filename, 'w') as file:
                json.dump(data, file, indent=2)
            return True
        except Exception as e:
            print(f"Error saving to {filename}: {e}")
            return False
    
    def load_json(self, filename: str) -> Dict:
        """Load data from JSON file"""
        try:
            if os.path.exists(filename):
                with open(filename, 'r') as file:
                    return json.load(file)
            return {}
        except Exception as e:
            print(f"Error loading {filename}: {e}")
            return {}
    
    # Student operations
    def load_students(self) -> List[Dict]:
        """Load all students"""
        data = self.load_json(self.students_file)
        return data.get("students", [])
    
    def save_student(self, student: Dict) -> bool:
        """Save a new student"""
        data = self.load_json(self.students_file)
        students = data.get("students", [])
        students.append(student)
        data["students"] = students
        return self.save_json(self.students_file, data)
    
    def update_student(self, updated_student: Dict) -> bool:
        """Update existing student"""
        data = self.load_json(self.students_file)
        students = data.get("students", [])
        
        for i, student in enumerate(students):
            if student["student_id"] == updated_student["student_id"]:
                students[i] = updated_student
                data["students"] = students
                return self.save_json(self.students_file, data)
        return False
    
    # Book operations
    def load_books(self) -> List[Dict]:
        """Load all books"""
        data = self.load_json(self.books_file)
        return data.get("books", [])
    
    def save_book(self, book: Dict) -> bool:
        """Save a new book"""
        data = self.load_json(self.books_file)
        books = data.get("books", [])
        books.append(book)
        data["books"] = books
        data["next_book_id"] = data.get("next_book_id", 1) + 1
        return self.save_json(self.books_file, data)
    
    def update_book(self, updated_book: Dict) -> bool:
        """Update existing book"""
        data = self.load_json(self.books_file)
        books = data.get("books", [])
        
        for i, book in enumerate(books):
            if book["book_id"] == updated_book["book_id"]:
                books[i] = updated_book
                data["books"] = books
                return self.save_json(self.books_file, data)
        return False
    
    def get_next_book_id(self) -> int:
        """Get next available book ID"""
        data = self.load_json(self.books_file)
        return data.get("next_book_id", 1)
    
    # Logging operations
    def log_activity(self, user_id: str, action: str, details: str = "") -> bool:
        """Log user activity"""
        data = self.load_json(self.logs_file)
        logs = data.get("logs", [])
        
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "user_id": user_id,
            "action": action,
            "details": details
        }
        
        logs.append(log_entry)
        data["logs"] = logs
        return self.save_json(self.logs_file, data)
    
    def get_logs(self, user_id: str = None) -> List[Dict]:
        """Get activity logs, optionally filtered by user"""
        data = self.load_json(self.logs_file)
        logs = data.get("logs", [])
        
        if user_id:
            return [log for log in logs if log["user_id"] == user_id]
        return logs


# ============== SONIA'S MODULE: student.py ==============
from typing import List, Dict, Optional, Tuple

class StudentManager:
    """
    Sonia's Student Manager - All student-specific functionality
    """
    
    def __init__(self, storage_manager: StorageManager):
        self.storage = storage_manager
        self.current_student = None
    
    # Registration & Login
    def register_student(self, student_id: str, name: str, email: str = "") -> Tuple[bool, str]:
        """Register a new student"""
        if not student_id.strip() or not name.strip():
            return False, "Student ID and name cannot be empty"
        
        existing_students = self.storage.load_students()
        if any(s["student_id"] == student_id for s in existing_students):
            return False, f"Student ID '{student_id}' already exists"
        
        new_student = {
            "student_id": student_id,
            "name": name,
            "email": email,
            "user_type": "student",
            "borrowed_books": [],
            "favorites": [],
            "registration_date": datetime.now().isoformat()
        }
        
        if self.storage.save_student(new_student):
            self.storage.log_activity(student_id, "REGISTER", f"New student: {name}")
            return True, f"Registration successful! Welcome, {name}"
        return False, "Registration failed"
    
    def login_student(self, student_id: str) -> Tuple[bool, str, Optional[Dict]]:
        """Login student"""
        students = self.storage.load_students()
        student = next((s for s in students if s["student_id"] == student_id), None)
        
        if student:
            self.current_student = student
            self.storage.log_activity(student_id, "LOGIN", "Student login")
            return True, f"Welcome back, {student['name']}", student
        return False, "Student ID not found", None
    
    def logout_student(self) -> str:
        """Logout current student"""
        if self.current_student:
            self.storage.log_activity(self.current_student["student_id"], "LOGOUT", "Student logout")
            name = self.current_student["name"]
            self.current_student = None
            return f"Goodbye, {name}!"
        return "No student logged in"
    
    # Browse Categories
    def get_all_categories(self) -> List[str]:
        """Get all book categories"""
        books = self.storage.load_books()
        categories = set(book["category"] for book in books)
        return sorted(list(categories))
    
    def get_books_by_category(self, category: str) -> List[Dict]:
        """Get books in specific category"""
        books = self.storage.load_books()
        return [book for book in books if book["category"].lower() == category.lower()]
    
    # Search Functionality
    def search_books(self, query: str = "", category: str = "", available_only: bool = False) -> List[Dict]:
        """Search books by various criteria"""
        books = self.storage.load_books()
        results = []
        
        for book in books:
            # Category filter
            if category and book["category"].lower() != category.lower():
                continue
            
            # Query filter
            if query:
                query_lower = query.lower()
                if (query_lower not in book["title"].lower() and 
                    query_lower not in book["author"].lower()):
                    continue
            
            # Available filter
            if available_only and book["available_copies"] <= 0:
                continue
            
            results.append(book)
        
        return results
    
    # Favorites Management
    def add_to_favorites(self, book_id: int) -> Tuple[bool, str]:
        """Add book to favorites"""
        if not self.current_student:
            return False, "Please login first"
        
        books = self.storage.load_books()
        book = next((b for b in books if b["book_id"] == book_id), None)
        if not book:
            return False, "Book not found"
        
        if book_id in self.current_student["favorites"]:
            return False, "Book already in favorites"
        
        self.current_student["favorites"].append(book_id)
        self.storage.update_student(self.current_student)
        self.storage.log_activity(self.current_student["student_id"], "ADD_FAVORITE", f"Book: {book['title']}")
        return True, f"'{book['title']}' added to favorites"
    
    def remove_from_favorites(self, book_id: int) -> Tuple[bool, str]:
        """Remove book from favorites"""
        if not self.current_student:
            return False, "Please login first"
        
        if book_id not in self.current_student["favorites"]:
            return False, "Book not in favorites"
        
        books = self.storage.load_books()
        book = next((b for b in books if b["book_id"] == book_id), None)
        book_title = book["title"] if book else f"Book ID {book_id}"
        
        self.current_student["favorites"].remove(book_id)
        self.storage.update_student(self.current_student)
        self.storage.log_activity(self.current_student["student_id"], "REMOVE_FAVORITE", f"Book: {book_title}")
        return True, f"'{book_title}' removed from favorites"
    
    def get_favorites(self) -> List[Dict]:
        """Get student's favorite books"""
        if not self.current_student:
            return []
        
        books = self.storage.load_books()
        favorite_ids = self.current_student["favorites"]
        return [book for book in books if book["book_id"] in favorite_ids]


# ============== WALIYAT'S MODULE: admin.py ==============
class AdminManager:
    """
    Waliyat's Admin Manager - All admin-specific functionality
    """
    
    def __init__(self, storage_manager: StorageManager):
        self.storage = storage_manager
        self.current_admin = None
    
    def login_admin(self, admin_id: str) -> Tuple[bool, str, Optional[Dict]]:
        """Login admin user"""
        students = self.storage.load_students()  # Admins stored with students
        admin = next((s for s in students if s["student_id"] == admin_id and s["user_type"] == "admin"), None)
        
        if admin:
            self.current_admin = admin
            self.storage.log_activity(admin_id, "ADMIN_LOGIN", "Admin login")
            return True, f"Admin login successful. Welcome, {admin['name']}", admin
        return False, "Admin not found", None
    
    def add_book(self, title: str, author: str, category: str, copies: int = 1) -> Tuple[bool, str]:
        """Add new book to library"""
        if not self.current_admin:
            return False, "Admin login required"
        
        if not all([title.strip(), author.strip(), category.strip()]) or copies < 1:
            return False, "Invalid book data"
        
        book_id = self.storage.get_next_book_id()
        new_book = {
            "book_id": book_id,
            "title": title,
            "author": author,
            "category": category,
            "total_copies": copies,
            "available_copies": copies,
            "borrowed_by": []
        }
        
        if self.storage.save_book(new_book):
            self.storage.log_activity(self.current_admin["student_id"], "ADD_BOOK", 
                                    f"Added: {title} by {author}")
            return True, f"Book '{title}' added successfully (ID: {book_id})"
        return False, "Failed to add book"
    
    def edit_book(self, book_id: int, title: str = None, author: str = None, 
                  category: str = None, total_copies: int = None) -> Tuple[bool, str]:
        """Edit existing book"""
        if not self.current_admin:
            return False, "Admin login required"
        
        books = self.storage.load_books()
        book = next((b for b in books if b["book_id"] == book_id), None)
        if not book:
            return False, "Book not found"
        
        # Update fields if provided
        if title: book["title"] = title
        if author: book["author"] = author
        if category: book["category"] = category
        if total_copies is not None:
            # Adjust available copies proportionally
            borrowed = book["total_copies"] - book["available_copies"]
            book["total_copies"] = total_copies
            book["available_copies"] = max(0, total_copies - borrowed)
        
        if self.storage.update_book(book):
            self.storage.log_activity(self.current_admin["student_id"], "EDIT_BOOK", 
                                    f"Edited book ID: {book_id}")
            return True, f"Book '{book['title']}' updated successfully"
        return False, "Failed to update book"
    
    def manage_user(self, user_id: str, action: str) -> Tuple[bool, str]:
        """Manage user accounts (activate/deactivate)"""
        if not self.current_admin:
            return False, "Admin login required"
        
        students = self.storage.load_students()
        user = next((s for s in students if s["student_id"] == user_id), None)
        if not user:
            return False, "User not found"
        
        if action == "activate":
            user["status"] = "active"
            message = f"User {user_id} activated"
        elif action == "deactivate":
            user["status"] = "inactive"
            message = f"User {user_id} deactivated"
        else:
            return False, "Invalid action"
        
        if self.storage.update_student(user):
            self.storage.log_activity(self.current_admin["student_id"], "MANAGE_USER", message)
            return True, message
        return False, "Failed to update user"
    
    def get_all_users(self) -> List[Dict]:
        """Get all users for management"""
        return self.storage.load_students()
    
    def get_all_books(self) -> List[Dict]:
        """Get all books for management"""
        return self.storage.load_books()
    
    def get_system_stats(self) -> Dict:
        """Get system statistics"""
        books = self.storage.load_books()
        students = self.storage.load_students()
        
        total_books = len(books)
        available_books = sum(1 for book in books if book["available_copies"] > 0)
        total_students = sum(1 for user in students if user["user_type"] == "student")
        
        return {
            "total_books": total_books,
            "available_books": available_books,
            "borrowed_books": total_books - available_books,
            "total_students": total_students,
            "active_borrowers": sum(1 for user in students 
                                  if user["user_type"] == "student" and user["borrowed_books"])
        }


# ============== TRESOR'S MODULE: cli.py ==============
class CLIManager:
    """
    Tresor's CLI Manager - All menus and user interface
    """
    
    def __init__(self, storage_manager: StorageManager):
        self.storage = storage_manager
        self.student_manager = StudentManager(storage_manager)
        self.admin_manager = AdminManager(storage_manager)
    
    def display_welcome(self):
        """Display welcome screen"""
        print("\n" + "="*60)
        print("          🏛️  LIBRARY MANAGEMENT SYSTEM  📚")
        print("="*60)
        print("         Welcome to Digital Library Portal")
        print("="*60)
    
    def get_user_input(self, prompt: str) -> str:
        """Get user input with prompt"""
        return input(f"{prompt}: ").strip()
    
    def display_message(self, message: str, msg_type: str = "info"):
        """Display formatted message"""
        symbols = {"info": "ℹ️", "success": "✅", "error": "❌", "warning": "⚠️"}
        symbol = symbols.get(msg_type, "ℹ️")
        print(f"\n{symbol} {message}")
    
    def select_role(self) -> str:
        """Role selection menu"""
        while True:
            print("\n📋 Select your role:")
            print("1. 👨‍🎓 Student")
            print("2. 👨‍💼 Administrator")
            print("3. 🚪 Exit")
            
            choice = self.get_user_input("Enter choice (1-3)")
            
            if choice == "1":
                return "student"
            elif choice == "2":
                return "admin"
            elif choice == "3":
                return "exit"
            else:
                self.display_message("Invalid choice! Please try again.", "error")
    
    def student_flow(self):
        """Handle complete student workflow"""
        while True:
            if not self.student_manager.current_student:
                # Student login/registration menu
                print("\n👨‍🎓 STUDENT PORTAL")
                print("1. 📝 Register")
                print("2. 🔐 Login")
                print("3. ⬅️ Back to main menu")
                
                choice = self.get_user_input("Enter choice")
                
                if choice == "1":
                    self.handle_student_registration()
                elif choice == "2":
                    self.handle_student_login()
                elif choice == "3":
                    break
                else:
                    self.display_message("Invalid choice!", "error")
            else:
                # Student main menu
                self.display_student_dashboard()
                print("\n📚 What would you like to do?")
                print("1. 🗂️  Browse Categories")
                print("2. 🔍 Search Books")
                print("3. ❤️  My Favorites")
                print("4. 📊 My Profile")
                print("5. 🚪 Logout")
                
                choice = self.get_user_input("Enter choice")
                
                if choice == "1":
                    self.handle_browse_categories()
                elif choice == "2":
                    self.handle_search_books()
                elif choice == "3":
                    self.handle_favorites()
                elif choice == "4":
                    self.display_student_profile()
                elif choice == "5":
                    message = self.student_manager.logout_student()
                    self.display_message(message, "info")
                else:
                    self.display_message("Invalid choice!", "error")
    
    def handle_student_registration(self):
        """Handle student registration"""
        print("\n📝 STUDENT REGISTRATION")
        student_id = self.get_user_input("Enter Student ID")
        name = self.get_user_input("Enter Full Name")
        email = self.get_user_input("Enter Email (optional)")
        
        success, message = self.student_manager.register_student(student_id, name, email)
        msg_type = "success" if success else "error"
        self.display_message(message, msg_type)
        
        if success:
            # Auto-login after registration
            self.student_manager.login_student(student_id)
    
    def handle_student_login(self):
        """Handle student login"""
        print("\n🔐 STUDENT LOGIN")
        student_id = self.get_user_input("Enter Student ID")
        
        success, message, student_data = self.student_manager.login_student(student_id)
        msg_type = "success" if success else "error"
        self.display_message(message, msg_type)
    
    def display_student_dashboard(self):
        """Display student dashboard"""
        student = self.student_manager.current_student
        print(f"\n👨‍🎓 Welcome, {student['name']}!")
        print(f"📚 Borrowed Books: {len(student['borrowed_books'])}")
        print(f"❤️  Favorite Books: {len(student['favorites'])}")
    
    def handle_browse_categories(self):
        """Handle category browsing"""
        categories = self.student_manager.get_all_categories()
        
        if not categories:
            self.display_message("No categories available", "info")
            return
        
        print("\n🗂️  BROWSE CATEGORIES")
        for i, category in enumerate(categories, 1):
            books_in_cat = self.student_manager.get_books_by_category(category)
            print(f"{i}. {category} ({len(books_in_cat)} books)")
        
        try:
            choice = int(self.get_user_input(f"Select category (1-{len(categories)})"))
            if 1 <= choice <= len(categories):
                selected_category = categories[choice - 1]
                books = self.student_manager.get_books_by_category(selected_category)
                self.display_book_list(books, f"Books in '{selected_category}' category")
                self.handle_book_actions(books)
            else:
                self.display_message("Invalid category selection!", "error")
        except ValueError:
            self.display_message("Please enter a valid number!", "error")
    
    def handle_search_books(self):
        """Handle book search"""
        print("\n🔍 SEARCH BOOKS")
        print("1. Search by title/author")
        print("2. Search by category")
        print("3. Show available books only")
        
        search_type = self.get_user_input("Select search type")
        
        if search_type == "1":
            query = self.get_user_input("Enter title or author")
            results = self.student_manager.search_books(query=query)
        elif search_type == "2":
            categories = self.student_manager.get_all_categories()
            for i, cat in enumerate(categories, 1):
                print(f"{i}. {cat}")
            try:
                cat_choice = int(self.get_user_input("Select category"))
                if 1 <= cat_choice <= len(categories):
                    category = categories[cat_choice - 1]
                    results = self.student_manager.search_books(category=category)
                else:
                    self.display_message("Invalid category!", "error")
                    return
            except ValueError:
                self.display_message("Invalid input!", "error")
                return
        elif search_type == "3":
            results = self.student_manager.search_books(available_only=True)
        else:
            self.display_message("Invalid search type!", "error")
            return
        
        self.display_book_list(results, "Search Results")
        if results:
            self.handle_book_actions(results)
    
    def handle_favorites(self):
        """Handle favorites management"""
        favorites = self.student_manager.get_favorites()
        
        if not favorites:
            self.display_message("You have no favorite books yet!", "info")
            return
        
        self.display_book_list(favorites, "Your Favorite Books")
        
        print("\n❤️  FAVORITES ACTIONS")
        print("1. Remove from favorites")
        print("2. Search within favorites")
        print("3. Back to main menu")
        
        choice = self.get_user_input("Enter choice")
        
        if choice == "1":
            try:
                book_id = int(self.get_user_input("Enter book ID to remove"))
                success, message = self.student_manager.remove_from_favorites(book_id)
                msg_type = "success" if success else "error"
                self.display_message(message, msg_type)
            except ValueError:
                self.display_message("Invalid book ID!", "error")
        elif choice == "2":
            query = self.get_user_input("Search within favorites")
            # Implementation would use search within favorites
            self.display_message("Search in favorites feature", "info")
    
    def handle_book_actions(self, books: List[Dict]):
        """Handle actions on book list"""
        if not books:
            return
        
        print("\n📖 BOOK ACTIONS")
        print("1. Add book to favorites")
        print("2. View book details")
        print("3. Back to menu")
        
        choice = self.get_user_input("Enter choice")
        
        if choice == "1":
            try:
                book_id = int(self.get_user_input("Enter book ID to add to favorites"))
                success, message = self.student_manager.add_to_favorites(book_id)
                msg_type = "success" if success else "error"
                self.display_message(message, msg_type)
            except ValueError:
                self.display_message("Invalid book ID!", "error")
        elif choice == "2":
            try:
                book_id = int(self.get_user_input("Enter book ID for details"))
                book = next((b for b in books if b["book_id"] == book_id), None)
                if book:
                    self.display_book_details(book)
                else:
                    self.display_message("Book not found!", "error")
            except ValueError:
                self.display_message("Invalid book ID!", "error")
    
    def display_book_list(self, books: List[Dict], title: str):
        """Display formatted book list"""
        if not books:
            self.display_message(f"No books found for {title.lower()}", "info")
            return
        
        print(f"\n📚 {title} ({len(books)} books)")
        print("="*80)
        print(f"{'ID':<5} {'Title':<30} {'Author':<20} {'Category':<15} {'Available'}")
        print("="*80)
        
        for book in books:
            available = book["available_copies"]
            total = book["total_copies"]
            status = f"{available}/{total}" if available > 0 else "None"
            
            print(f"{book['book_id']:<5} {book['title'][:29]:<30} {book['author'][:19]:<20} "
                  f"{book['category'][:14]:<15} {status}")
        print("="*80)
    
    def display_book_details(self, book: Dict):
        """Display detailed book information"""
        print(f"\n📖 BOOK DETAILS")
        print("="*50)
        print(f"📚 Title: {book['title']}")
        print(f"✍️  Author: {book['author']}")
        print(f"📂 Category: {book['category']}")
        print(f"🆔 Book ID: {book['book_id']}")
        print(f"📊 Copies: {book['available_copies']} available / {book['total_copies']} total")
        print("="*50)
    
    def display_student_profile(self):
        """Display student profile"""
        student = self.student_manager.current_student
        print(f"\n👤 STUDENT PROFILE")
        print("="*40)
        print(f"🆔 Student ID: {student['student_id']}")
        print(f"👤 Name: {student['name']}")
        print(f"📧 Email: {student.get('email', 'Not provided')}")
        print(f"📅 Member since: {student['registration_date'][:10]}")
        print(f"📚 Borrowed books: {len(student['borrowed_books'])}")
        print(f"❤️  Favorite books: {len(student['favorites'])}")
        print("="*40)
    
    def admin_flow(self):
        """Handle complete admin workflow"""
        while True:
            if not self.admin_manager.current_admin:
                # Admin login menu
                print("\n👨‍💼 ADMIN PORTAL")
                print("1. 🔐 Login")
                print("2. ⬅️ Back to main menu")
                
                choice = self.get_user_input("Enter choice")
                
                if choice == "1":
                    self.handle_admin_login()
                elif choice == "2":
                    break
                else:
                    self.display_message("Invalid choice!", "error")
            else:
                # Admin main menu
                self.display_admin_dashboard()
                print("\n🛠️ Admin Actions:")
                print("1. 📚 Add New Book")
                print("2. ✏️ Edit Book")
                print("3. 👥 Manage Users")
                print("4. 📊 View System Stats")
                print("5. 📋 View All Books")
                print("6. 👨‍🎓 View All Students")
                print("7. 📜 View Activity Logs")
                print("8. 🚪 Logout")
                
                choice = self.get_user_input("Enter choice")
                
                if choice == "1":
                    self.handle_add_book()
                elif choice == "2":
                    self.handle_edit_book()
                elif choice == "3":
                    self.handle_manage_users()
                elif choice == "4":
                    self.display_system_stats()
                elif choice == "5":
                    self.display_all_books_admin()
                elif choice == "6":
                    self.display_all_students()
                elif choice == "7":
                    self.display_activity_logs()
                elif choice == "8":
                    message = self.admin_manager.logout_admin()
                    self.display_message(message, "info")
                else:
                    self.display_message("Invalid choice!", "error")
    
    def handle_admin_login(self):
        """Handle admin login"""
        print("\n🔐 ADMIN LOGIN")
        admin_id = self.get_user_input("Enter Admin ID")
        
        success, message, admin_data = self.admin_manager.login_admin(admin_id)
        msg_type = "success" if success else "error"
        self.display_message(message, msg_type)
    
    def display_admin_dashboard(self):
        """Display admin dashboard"""
        admin = self.admin_manager.current_admin
        stats = self.admin_manager.get_system_stats()
        
        print(f"\n👨‍💼 Admin Dashboard - Welcome, {admin['name']}!")
        print(f"📚 Total Books: {stats['total_books']}")
        print(f"✅ Available: {stats['available_books']}")
        print(f"📖 Borrowed: {stats['borrowed_books']}")
        print(f"👨‍🎓 Total Students: {stats['total_students']}")
    
    def handle_add_book(self):
        """Handle adding new book"""
        print("\n📚 ADD NEW BOOK")
        title = self.get_user_input("Enter book title")
        author = self.get_user_input("Enter author name")
        category = self.get_user_input("Enter category")
        
        try:
            copies = int(self.get_user_input("Enter number of copies"))
            success, message = self.admin_manager.add_book(title, author, category, copies)
            msg_type = "success" if success else "error"
            self.display_message(message, msg_type)
        except ValueError:
            self.display_message("Invalid number of copies!", "error")
    
    def handle_edit_book(self):
        """Handle editing existing book"""
        books = self.admin_manager.get_all_books()
        self.display_book_list(books, "All Books - Select to Edit")
        
        try:
            book_id = int(self.get_user_input("Enter book ID to edit"))
            book = next((b for b in books if b["book_id"] == book_id), None)
            
            if not book:
                self.display_message("Book not found!", "error")
                return
            
            print(f"\nEditing: {book['title']}")
            print("(Press Enter to keep current value)")
            
            new_title = self.get_user_input(f"Title [{book['title']}]") or book['title']
            new_author = self.get_user_input(f"Author [{book['author']}]") or book['author']
            new_category = self.get_user_input(f"Category [{book['category']}]") or book['category']
            
            copies_input = self.get_user_input(f"Total copies [{book['total_copies']}]")
            new_copies = int(copies_input) if copies_input else book['total_copies']
            
            success, message = self.admin_manager.edit_book(
                book_id, new_title, new_author, new_category, new_copies)
            msg_type = "success" if success else "error"
            self.display_message(message, msg_type)
            
        except ValueError:
            self.display_message("Invalid input!", "error")
    
    def handle_manage_users(self):
        """Handle user management"""
        users = self.admin_manager.get_all_users()
        students = [u for u in users if u["user_type"] == "student"]
        
        if not students:
            self.display_message("No students found!", "info")
            return
        
        print("\n👥 MANAGE USERS")
        print("="*70)
        print(f"{'ID':<15} {'Name':<25} {'Email':<25} {'Status'}")
        print("="*70)
        
        for student in students:
            status = student.get("status", "active")
            print(f"{student['student_id']:<15} {student['name'][:24]:<25} "
                  f"{student.get('email', 'N/A')[:24]:<25} {status}")
        print("="*70)
        
        user_id = self.get_user_input("Enter user ID to manage")
        print("1. Activate user")
        print("2. Deactivate user")
        
        action_choice = self.get_user_input("Select action")
        action = "activate" if action_choice == "1" else "deactivate" if action_choice == "2" else None
        
        if action:
            success, message = self.admin_manager.manage_user(user_id, action)
            msg_type = "success" if success else "error"
            self.display_message(message, msg_type)
        else:
            self.display_message("Invalid action!", "error")
    
    def display_system_stats(self):
        """Display system statistics"""
        stats = self.admin_manager.get_system_stats()
        
        print("\n📊 SYSTEM STATISTICS")
        print("="*40)
        print(f"📚 Total Books: {stats['total_books']}")
        print(f"✅ Available Books: {stats['available_books']}")
        print(f"📖 Currently Borrowed: {stats['borrowed_books']}")
        print(f"👨‍🎓 Total Students: {stats['total_students']}")
        print(f"🔄 Active Borrowers: {stats['active_borrowers']}")
        print("="*40)
        
        # Calculate percentages
        if stats['total_books'] > 0:
            availability_rate = (stats['available_books'] / stats['total_books']) * 100
            print(f"📈 Book Availability: {availability_rate:.1f}%")
        
        if stats['total_students'] > 0:
            borrowing_rate = (stats['active_borrowers'] / stats['total_students']) * 100
            print(f"📈 Student Engagement: {borrowing_rate:.1f}%")
    
    def display_all_books_admin(self):
        """Display all books for admin with detailed info"""
        books = self.admin_manager.get_all_books()
        
        print("\n📚 ALL BOOKS - ADMIN VIEW")
        print("="*90)
        print(f"{'ID':<5} {'Title':<25} {'Author':<20} {'Category':<15} {'Copies':<10} {'Borrowed By'}")
        print("="*90)
        
        for book in books:
            borrowed_count = len(book['borrowed_by'])
            copies_info = f"{book['available_copies']}/{book['total_copies']}"
            borrowed_by = ', '.join(book['borrowed_by'][:3]) if book['borrowed_by'] else "None"
            if len(book['borrowed_by']) > 3:
                borrowed_by += "..."
            
            print(f"{book['book_id']:<5} {book['title'][:24]:<25} {book['author'][:19]:<20} "
                  f"{book['category'][:14]:<15} {copies_info:<10} {borrowed_by}")
        print("="*90)
    
    def display_all_students(self):
        """Display all students for admin"""
        users = self.admin_manager.get_all_users()
        students = [u for u in users if u["user_type"] == "student"]
        
        print("\n👨‍🎓 ALL STUDENTS")
        print("="*80)
        print(f"{'ID':<15} {'Name':<25} {'Borrowed':<10} {'Favorites':<10} {'Joined'}")
        print("="*80)
        
        for student in students:
            borrowed_count = len(student['borrowed_books'])
            favorites_count = len(student['favorites'])
            join_date = student['registration_date'][:10]
            
            print(f"{student['student_id']:<15} {student['name'][:24]:<25} "
                  f"{borrowed_count:<10} {favorites_count:<10} {join_date}")
        print("="*80)
    
    def display_activity_logs(self):
        """Display recent activity logs"""
        logs = self.storage.get_logs()
        recent_logs = logs[-20:] if len(logs) > 20 else logs  # Show last 20 logs
        
        print("\n📜 RECENT ACTIVITY LOGS")
        print("="*90)
        print(f"{'Time':<20} {'User':<15} {'Action':<15} {'Details'}")
        print("="*90)
        
        for log in reversed(recent_logs):  # Show most recent first
            timestamp = log['timestamp'][:19].replace('T', ' ')
            user_id = log['user_id']
            action = log['action']
            details = log.get('details', '')[:40]
            
            print(f"{timestamp:<20} {user_id:<15} {action:<15} {details}")
        print("="*90)


# ============== CHRISTIAN'S MODULE: main.py ==============
class LibraryApp:
    """
    Christian's Main Application - Integrates all modules and controls program flow
    """
    
    def __init__(self):
        self.storage = StorageManager()
        self.cli = CLIManager(self.storage)
        self.running = True
    
    def run(self):
        """Main application loop"""
        try:
            self.cli.display_welcome()
            
            while self.running:
                role = self.cli.select_role()
                
                if role == "student":
                    self.cli.student_flow()
                elif role == "admin":
                    self.cli.admin_flow()
                elif role == "exit":
                    self.shutdown()
                    break
                
        except KeyboardInterrupt:
            print("\n\n👋 Thank you for using the Library Management System!")
            self.shutdown()
        except Exception as e:
            print(f"\n❌ An unexpected error occurred: {e}")
            self.shutdown()
    
    def shutdown(self):
        """Clean shutdown of the application"""
        print("\n🔄 Saving data and shutting down...")
        self.running = False
        print("✅ Goodbye!")


# ============== DARLENE'S MODULE: test_library.py ==============
import unittest
from unittest.mock import patch, MagicMock

class TestStudentManager(unittest.TestCase):
    """
    Darlene's Unit Tests for Student Manager
    """
    
    def setUp(self):
        """Set up test fixtures"""
        self.mock_storage = MagicMock()
        self.student_manager = StudentManager(self.mock_storage)
    
    def test_register_student_success(self):
        """Test successful student registration"""
        # Mock storage to return empty list (no existing students)
        self.mock_storage.load_students.return_value = []
        self.mock_storage.save_student.return_value = True
        
        success, message = self.student_manager.register_student("test123", "Test Student", "test@email.com")
        
        self.assertTrue(success)
        self.assertIn("Registration successful", message)
        self.mock_storage.save_student.assert_called_once()
    
    def test_register_duplicate_student(self):
        """Test registration with duplicate student ID"""
        # Mock storage to return existing student
        existing_student = {"student_id": "test123", "name": "Existing Student"}
        self.mock_storage.load_students.return_value = [existing_student]
        
        success, message = self.student_manager.register_student("test123", "New Student")
        
        self.assertFalse(success)
        self.assertIn("already exists", message)
    
    def test_login_student_success(self):
        """Test successful student login"""
        student_data = {
            "student_id": "test123",
            "name": "Test Student",
            "user_type": "student",
            "borrowed_books": [],
            "favorites": []
        }
        self.mock_storage.load_students.return_value = [student_data]
        
        success, message, returned_data = self.student_manager.login_student("test123")
        
        self.assertTrue(success)
        self.assertIn("Welcome back", message)
        self.assertEqual(returned_data, student_data)
        self.assertEqual(self.student_manager.current_student, student_data)
    
    def test_search_books(self):
        """Test book search functionality"""
        mock_books = [
            {"book_id": 1, "title": "Python Programming", "author": "John Doe", "category": "Programming"},
            {"book_id": 2, "title": "Java Basics", "author": "Jane Smith", "category": "Programming"},
            {"book_id": 3, "title": "Data Science", "author": "Bob Johnson", "category": "Science"}
        ]
        self.mock_storage.load_books.return_value = mock_books
        
        # Test search by query
        results = self.student_manager.search_books(query="Python")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["title"], "Python Programming")
        
        # Test search by category
        results = self.student_manager.search_books(category="Programming")
        self.assertEqual(len(results), 2)
    
    def test_add_to_favorites(self):
        """Test adding book to favorites"""
        # Set up current student
        student_data = {
            "student_id": "test123",
            "name": "Test Student",
            "favorites": []
        }
        self.student_manager.current_student = student_data
        
        # Mock book exists
        mock_books = [{"book_id": 1, "title": "Test Book"}]
        self.mock_storage.load_books.return_value = mock_books
        self.mock_storage.update_student.return_value = True
        
        success, message = self.student_manager.add_to_favorites(1)
        
        self.assertTrue(success)
        self.assertIn("added to favorites", message)
        self.assertIn(1, student_data["favorites"])


class TestAdminManager(unittest.TestCase):
    """
    Darlene's Unit Tests for Admin Manager
    """
    
    def setUp(self):
        """Set up test fixtures"""
        self.mock_storage = MagicMock()
        self.admin_manager = AdminManager(self.mock_storage)
    
    def test_add_book_success(self):
        """Test successful book addition"""
        # Set up current admin
        admin_data = {"student_id": "admin", "name": "Admin User"}
        self.admin_manager.current_admin = admin_data
        
        self.mock_storage.get_next_book_id.return_value = 10
        self.mock_storage.save_book.return_value = True
        
        success, message = self.admin_manager.add_book("Test Book", "Test Author", "Test Category", 2)
        
        self.assertTrue(success)
        self.assertIn("added successfully", message)
        self.mock_storage.save_book.assert_called_once()
    
    def test_add_book_no_admin(self):
        """Test book addition without admin login"""
        success, message = self.admin_manager.add_book("Test Book", "Test Author", "Test Category")
        
        self.assertFalse(success)
        self.assertIn("Admin login required", message)


class TestStorageManager(unittest.TestCase):
    """
    Darlene's Unit Tests for Storage Manager
    """
    
    @patch('os.path.exists')
    @patch('builtins.open')
    @patch('json.load')
    def test_load_students(self, mock_json_load, mock_open, mock_exists):
        """Test loading students from file"""
        mock_exists.return_value = True
        mock_json_load.return_value = {
            "students": [
                {"student_id": "test1", "name": "Student 1"},
                {"student_id": "test2", "name": "Student 2"}
            ]
        }
        
        storage = StorageManager()
        students = storage.load_students()
        
        self.assertEqual(len(students), 2)
        self.assertEqual(students[0]["student_id"], "test1")
    
    @patch('builtins.open')
    @patch('json.dump')
    def test_save_student(self, mock_json_dump, mock_open):
        """Test saving student to file"""
        storage = StorageManager()
        storage.load_json = MagicMock(return_value={"students": []})
        storage.save_json = MagicMock(return_value=True)
        
        test_student = {"student_id": "test", "name": "Test Student"}
        result = storage.save_student(test_student)
        
        self.assertTrue(result)
        storage.save_json.assert_called_once()


# ============== APPLICATION ENTRY POINT ==============
def main():
    """
    Main entry point for the Library Management System
    """
    print("🚀 Initializing Library Management System...")
    
    try:
        app = LibraryApp()
        app.run()
    except Exception as e:
        print(f"❌ Failed to start application: {e}")
        print("Please check your installation and try again.")


# ============== USAGE EXAMPLES AND DOCUMENTATION ==============

"""
📚 LIBRARY MANAGEMENT SYSTEM - COMPLETE APPLICATION

This is the complete integrated library management system created by the team:

👥 TEAM CONTRIBUTIONS:
- Sonia (student.py): Student registration, login, search, favorites, browse categories
- Waliyat (admin.py): Admin functions, add/edit books, manage users, system stats
- Tresor (cli.py): All CLI menus, navigation, user interface, input handling
- Lea (storage.py): File operations, data persistence, JSON handling, logging
- Christian (main.py): Application integration, main program loop, coordination
- Darlene (test_library.py): Unit tests, quality assurance, README documentation

🚀 HOW TO RUN:
1. Save this entire code as different files (or use as single file)
2. Run: python main.py
3. Follow the interactive menu system

📁 FILE STRUCTURE:
library_management_system/
├── main.py           # Christian's main application
├── student.py        # Sonia's student functions
├── admin.py          # Waliyat's admin functions  
├── cli.py            # Tresor's CLI interface
├── storage.py        # Lea's storage system
├── test_library.py   # Darlene's unit tests
├── students.json     # Student data (auto-created)
├── books.json        # Book data (auto-created)
├── usage_logs.json   # Activity logs (auto-created)
└── README.md         # Documentation (Darlene's)

🔧 FEATURES:
Student Features:
- Registration and login
- Browse books by category
- Search books (multiple methods)
- Manage favorites list
- View personal profile

Admin Features:
- Add new books to library
- Edit existing books
- Manage user accounts
- View system statistics
- Monitor activity logs
- Comprehensive reporting

System Features:
- Data persistence (JSON files)
- Activity logging
- Error handling
- Input validation
- Comprehensive testing

💻 TECHNOLOGY STACK:
- Python 3.x
- JSON for data storage
- Object-oriented design
- Modular architecture
- Unit testing with unittest
- CLI-based interface

🔍 TESTING:
Run unit tests: python -m unittest test_library.py

📊 DEFAULT DATA:
- Admin account: ID "admin"
- Sample books in various categories
- Empty student database (register to create accounts)

🤝 INTEGRATION POINTS:
Each module communicates through well-defined interfaces:
- StorageManager handles all data operations
- StudentManager/AdminManager provide business logic
- CLIManager handles all user interaction
- Main app coordinates everything

This complete system demonstrates collaborative software development
with clear separation of concerns and proper integration patterns.
"""


if __name__ == "__main__":
    main()
