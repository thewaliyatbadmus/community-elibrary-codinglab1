# student.py - All Student Functions for Library Management System
import json
import os
from typing import List, Dict, Optional
from datetime import datetime

class Student:
    """Student class with all student-specific functionality"""
    
    def __init__(self, student_id: str, name: str, email: str = ""):
        self.student_id = student_id
        self.name = name
        self.email = email
        self.borrowed_books = []
        self.favorites = []
        self.registration_date = datetime.now().isoformat()
        self.is_logged_in = False
    
    def to_dict(self) -> Dict:
        """Convert student object to dictionary"""
        return {
            'student_id': self.student_id,
            'name': self.name,
            'email': self.email,
            'borrowed_books': self.borrowed_books,
            'favorites': self.favorites,
            'registration_date': self.registration_date
        }
    
    @classmethod
    def from_dict(cls, data: Dict):
        """Create student object from dictionary"""
        student = cls(data['student_id'], data['name'], data.get('email', ''))
        student.borrowed_books = data.get('borrowed_books', [])
        student.favorites = data.get('favorites', [])
        student.registration_date = data.get('registration_date', datetime.now().isoformat())
        return student

class StudentManager:
    """Manages all student operations and data"""
    
    def __init__(self, data_file: str = "students_data.json", books_file: str = "library_data.json"):
        self.data_file = data_file
        self.books_file = books_file
        self.students = {}
        self.current_student = None
        self.books_data = {}
        self.load_student_data()
        self.load_books_data()
    
    def load_student_data(self):
        """Load student data from file"""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r') as file:
                    data = json.load(file)
                    for student_data in data.get('students', []):
                        student = Student.from_dict(student_data)
                        self.students[student.student_id] = student
            except (json.JSONDecodeError, KeyError) as e:
                print(f"Error loading student data: {e}")
                self.students = {}
        else:
            self.students = {}
    
    def load_books_data(self):
        """Load books data from library file"""
        if os.path.exists(self.books_file):
            try:
                with open(self.books_file, 'r') as file:
                    data = json.load(file)
                    self.books_data = {book['book_id']: book for book in data.get('books', [])}
            except (json.JSONDecodeError, KeyError) as e:
                print(f"Error loading books data: {e}")
                self.books_data = {}
    
    def save_student_data(self):
        """Save student data to file"""
        data = {
            'students': [student.to_dict() for student in self.students.values()]
        }
        with open(self.data_file, 'w') as file:
            json.dump(data, file, indent=2)
    
    def register_student(self, student_id: str, name: str, email: str = "") -> bool:
        """Register a new student"""
        if student_id in self.students:
            print(f"Error: Student ID '{student_id}' already exists!")
            return False
        
        if not student_id.strip() or not name.strip():
            print("Error: Student ID and name cannot be empty!")
            return False
        
        # Create new student
        new_student = Student(student_id, name, email)
        self.students[student_id] = new_student
        self.save_student_data()
        
        print(f"Registration successful! Welcome, {name}")
        print(f"Your Student ID: {student_id}")
        return True
    
    def login_student(self, student_id: str) -> bool:
        """Login existing student"""
        if student_id not in self.students:
            print(f"Error: Student ID '{student_id}' not found!")
            print("Please register first or check your Student ID.")
            return False
        
        self.current_student = self.students[student_id]
        self.current_student.is_logged_in = True
        print(f"Login successful! Welcome back, {self.current_student.name}")
        return True
    
    def logout_student(self):
        """Logout current student"""
        if self.current_student:
            print(f"Goodbye, {self.current_student.name}!")
            self.current_student.is_logged_in = False
            self.current_student = None
        else:
            print("No student currently logged in.")
    
    def get_all_categories(self) -> List[str]:
        """Get all unique book categories"""
        categories = set()
        for book in self.books_data.values():
            categories.add(book['category'])
        return sorted(list(categories))
    
    def browse_categories(self):
        """Browse books by categories"""
        if not self.current_student:
            print("Please login first!")
            return
        
        categories = self.get_all_categories()
        if not categories:
            print("No categories available.")
            return
        
        print("\n" + "="*50)
        print("           BROWSE BY CATEGORIES")
        print("="*50)
        
        for i, category in enumerate(categories, 1):
            # Count books in each category
            book_count = sum(1 for book in self.books_data.values() 
                           if book['category'] == category)
            print(f"{i}. {category} ({book_count} books)")
        
        try:
            choice = int(input(f"\nSelect a category (1-{len(categories)}): "))
            if 1 <= choice <= len(categories):
                selected_category = categories[choice - 1]
                self.show_books_in_category(selected_category)
            else:
                print("Invalid category selection!")
        except ValueError:
            print("Invalid input! Please enter a number.")
    
    def show_books_in_category(self, category: str):
        """Show all books in a specific category"""
        books_in_category = [book for book in self.books_data.values() 
                           if book['category'] == category]
        
        if not books_in_category:
            print(f"No books found in '{category}' category.")
            return
        
        print(f"\n📚 Books in '{category}' Category ({len(books_in_category)} books):")
        print("-" * 80)
        print(f"{'ID':<5} {'Title':<35} {'Author':<25} {'Available':<10}")
        print("-" * 80)
        
        for book in books_in_category:
            available = book['available_copies']
            total = book['total_copies']
            status = f"{available}/{total}" if available > 0 else "Not Available"
            
            print(f"{book['book_id']:<5} {book['title'][:34]:<35} {book['author'][:24]:<25} {status:<10}")
        
        print("-" * 80)
        self.category_actions_menu(category, books_in_category)
    
    def category_actions_menu(self, category: str, books: List[Dict]):
        """Show action menu for category browsing"""
        print(f"\nActions for '{category}' category:")
        print("1. Add book to favorites")
        print("2. View book details")
        print("3. Search within this category")
        print("4. Back to categories")
        
        try:
            choice = int(input("Select an action: "))
            if choice == 1:
                self.add_to_favorites_from_list(books)
            elif choice == 2:
                self.view_book_details_from_list(books)
            elif choice == 3:
                self.search_within_category(category)
            elif choice == 4:
                return
            else:
                print("Invalid choice!")
        except ValueError:
            print("Invalid input!")
    
    def search_books(self, query: str = "", category: str = "") -> List[Dict]:
        """Search for books by title, author, or category"""
        if not query and not category:
            return list(self.books_data.values())
        
        results = []
        query_lower = query.lower() if query else ""
        category_lower = category.lower() if category else ""
        
        for book in self.books_data.values():
            # Check category match
            if category_lower and category_lower not in book['category'].lower():
                continue
            
            # Check query match in title or author
            if query_lower:
                if (query_lower not in book['title'].lower() and 
                    query_lower not in book['author'].lower()):
                    continue
            
            results.append(book)
        
        return results
    
    def search_interface(self):
        """Interactive search interface for students"""
        if not self.current_student:
            print("Please login first!")
            return
        
        print("\n" + "="*50)
        print("              SEARCH BOOKS")
        print("="*50)
        
        # Get search parameters
        print("Search Options:")
        print("1. Search by title/author")
        print("2. Search within a category")
        print("3. Advanced search")
        print("4. Show all available books")
        
        try:
            search_type = int(input("Select search type: "))
            
            if search_type == 1:
                query = input("Enter book title or author name: ").strip()
                results = self.search_books(query=query)
                self.display_search_results(results, f"Search results for '{query}'")
            
            elif search_type == 2:
                self.search_by_category()
            
            elif search_type == 3:
                self.advanced_search()
            
            elif search_type == 4:
                available_books = [book for book in self.books_data.values() 
                                 if book['available_copies'] > 0]
                self.display_search_results(available_books, "All Available Books")
            
            else:
                print("Invalid search type!")
                
        except ValueError:
            print("Invalid input! Please enter a number.")
    
    def search_by_category(self):
        """Search books within a specific category"""
        categories = self.get_all_categories()
        if not categories:
            print("No categories available.")
            return
        
        print("\nAvailable Categories:")
        for i, cat in enumerate(categories, 1):
            print(f"{i}. {cat}")
        
        try:
            choice = int(input("Select category: "))
            if 1 <= choice <= len(categories):
                selected_category = categories[choice - 1]
                query = input(f"Enter search term within '{selected_category}' (or press Enter for all): ").strip()
                results = self.search_books(query=query, category=selected_category)
                self.display_search_results(results, f"Results in '{selected_category}' category")
            else:
                print("Invalid category selection!")
        except ValueError:
            print("Invalid input!")
    
    def search_within_category(self, category: str):
        """Search within a specific category"""
        query = input(f"Search within '{category}' category: ").strip()
        results = self.search_books(query=query, category=category)
        self.display_search_results(results, f"Search results in '{category}'")
    
    def advanced_search(self):
        """Advanced search with multiple criteria"""
        print("\nAdvanced Search:")
        title_query = input("Book title (or press Enter to skip): ").strip()
        author_query = input("Author name (or press Enter to skip): ").strip()
        
        # Combine title and author queries
        combined_query = f"{title_query} {author_query}".strip()
        
        # Category selection
        categories = self.get_all_categories()
        print("\nSelect category (or press Enter to search all):")
        for i, cat in enumerate(categories, 1):
            print(f"{i}. {cat}")
        
        category = ""
        cat_input = input("Category number: ").strip()
        if cat_input.isdigit():
            idx = int(cat_input) - 1
            if 0 <= idx < len(categories):
                category = categories[idx]
        
        results = self.search_books(query=combined_query, category=category)
        search_desc = f"Advanced search results"
        if combined_query:
            search_desc += f" for '{combined_query}'"
        if category:
            search_desc += f" in '{category}' category"
        
        self.display_search_results(results, search_desc)
    
    def display_search_results(self, results: List[Dict], title: str):
        """Display search results in a formatted table"""
        if not results:
            print(f"\n❌ No books found for {title.lower()}.")
            return
        
        print(f"\n📖 {title} ({len(results)} books found):")
        print("=" * 90)
        print(f"{'ID':<5} {'Title':<30} {'Author':<20} {'Category':<15} {'Available':<10}")
        print("=" * 90)
        
        for book in results:
            available = book['available_copies']
            total = book['total_copies']
            status = f"{available}/{total}" if available > 0 else "❌ None"
            
            print(f"{book['book_id']:<5} {book['title'][:29]:<30} {book['author'][:19]:<20} "
                  f"{book['category'][:14]:<15} {status:<10}")
        
        print("=" * 90)
        self.search_results_actions(results)
    
    def search_results_actions(self, results: List[Dict]):
        """Actions menu for search results"""
        print("\nWhat would you like to do?")
        print("1. Add book to favorites")
        print("2. View book details")
        print("3. Filter results further")
        print("4. Back to main menu")
        
        try:
            choice = int(input("Select an action: "))
            if choice == 1:
                self.add_to_favorites_from_list(results)
            elif choice == 2:
                self.view_book_details_from_list(results)
            elif choice == 3:
                self.filter_results(results)
            elif choice == 4:
                return
            else:
                print("Invalid choice!")
        except ValueError:
            print("Invalid input!")
    
    def filter_results(self, results: List[Dict]):
        """Filter existing search results"""
        print("\nFilter current results by:")
        print("1. Available books only")
        print("2. Specific author")
        print("3. Books not in favorites")
        
        try:
            filter_choice = int(input("Select filter: "))
            filtered_results = results.copy()
            
            if filter_choice == 1:
                filtered_results = [book for book in results if book['available_copies'] > 0]
                self.display_search_results(filtered_results, "Available books from previous search")
            
            elif filter_choice == 2:
                author = input("Enter author name: ").strip().lower()
                filtered_results = [book for book in results if author in book['author'].lower()]
                self.display_search_results(filtered_results, f"Books by authors matching '{author}'")
            
            elif filter_choice == 3:
                filtered_results = [book for book in results 
                                  if book['book_id'] not in self.current_student.favorites]
                self.display_search_results(filtered_results, "Books not in your favorites")
            
            else:
                print("Invalid filter choice!")
                
        except ValueError:
            print("Invalid input!")
    
    def view_book_details_from_list(self, books: List[Dict]):
        """View detailed information about a specific book"""
        try:
            book_id = int(input("Enter book ID to view details: "))
            book = next((b for b in books if b['book_id'] == book_id), None)
            
            if not book:
                print("Book ID not found in current list!")
                return
            
            self.display_book_details(book)
            
        except ValueError:
            print("Invalid book ID!")
    
    def display_book_details(self, book: Dict):
        """Display detailed information about a book"""
        print("\n" + "="*60)
        print("                BOOK DETAILS")
        print("="*60)
        print(f"📚 Title: {book['title']}")
        print(f"✍️  Author: {book['author']}")
        print(f"📂 Category: {book['category']}")
        print(f"📊 Copies: {book['available_copies']} available out of {book['total_copies']} total")
        print(f"🆔 Book ID: {book['book_id']}")
        
        # Check if book is in favorites
        is_favorite = book['book_id'] in self.current_student.favorites
        print(f"❤️  Favorite: {'Yes' if is_favorite else 'No'}")
        
        # Check if book is borrowed by current student
        is_borrowed = book['book_id'] in self.current_student.borrowed_books
        print(f"📖 Status: {'Currently borrowed by you' if is_borrowed else 'Not borrowed by you'}")
        
        print("="*60)
        
        # Action options
        print("\nActions:")
        if not is_favorite:
            print("1. Add to favorites")
        else:
            print("1. Remove from favorites")
        print("2. Back to list")
        
        try:
            action = int(input("Select action: "))
            if action == 1:
                if not is_favorite:
                    self.add_to_favorites(book['book_id'])
                else:
                    self.remove_from_favorites(book['book_id'])
            elif action == 2:
                return
            else:
                print("Invalid action!")
        except ValueError:
            print("Invalid input!")
    
    def add_to_favorites(self, book_id: int) -> bool:
        """Add a book to student's favorites"""
        if not self.current_student:
            print("Please login first!")
            return False
        
        if book_id not in self.books_data:
            print("Book not found!")
            return False
        
        if book_id in self.current_student.favorites:
            print("Book is already in your favorites!")
            return False
        
        self.current_student.favorites.append(book_id)
        self.save_student_data()
        
        book_title = self.books_data[book_id]['title']
        print(f"✅ '{book_title}' added to your favorites!")
        return True
    
    def add_to_favorites_from_list(self, books: List[Dict]):
        """Add a book to favorites from a list of books"""
        try:
            book_id = int(input("Enter book ID to add to favorites: "))
            book = next((b for b in books if b['book_id'] == book_id), None)
            
            if not book:
                print("Book ID not found in current list!")
                return
            
            self.add_to_favorites(book_id)
            
        except ValueError:
            print("Invalid book ID!")
    
    def remove_from_favorites(self, book_id: int) -> bool:
        """Remove a book from student's favorites"""
        if not self.current_student:
            print("Please login first!")
            return False
        
        if book_id not in self.current_student.favorites:
            print("Book is not in your favorites!")
            return False
        
        self.current_student.favorites.remove(book_id)
        self.save_student_data()
        
        book_title = self.books_data[book_id]['title']
        print(f"❌ '{book_title}' removed from your favorites!")
        return True
    
    def view_favorites(self):
        """Display student's favorite books"""
        if not self.current_student:
            print("Please login first!")
            return
        
        if not self.current_student.favorites:
            print("\n❤️  You haven't added any books to your favorites yet!")
            print("Use the search or browse features to find books and add them to favorites.")
            return
        
        print(f"\n❤️  {self.current_student.name}'s Favorite Books ({len(self.current_student.favorites)} books):")
        print("=" * 80)
        print(f"{'ID':<5} {'Title':<35} {'Author':<25} {'Available':<10}")
        print("=" * 80)
        
        favorite_books = []
        for book_id in self.current_student.favorites:
            if book_id in self.books_data:
                book = self.books_data[book_id]
                favorite_books.append(book)
                
                available = book['available_copies']
                status = "✅ Available" if available > 0 else "❌ Not Available"
                
                print(f"{book['book_id']:<5} {book['title'][:34]:<35} {book['author'][:24]:<25} {status:<10}")
        
        print("=" * 80)
        
        if favorite_books:
            self.favorites_actions_menu(favorite_books)
    
    def favorites_actions_menu(self, favorite_books: List[Dict]):
        """Actions menu for favorites"""
        print("\nFavorites Actions:")
        print("1. Remove book from favorites")
        print("2. View book details")
        print("3. Search within favorites")
        print("4. Back to main menu")
        
        try:
            choice = int(input("Select an action: "))
            if choice == 1:
                self.remove_from_favorites_interface(favorite_books)
            elif choice == 2:
                self.view_book_details_from_list(favorite_books)
            elif choice == 3:
                self.search_within_favorites()
            elif choice == 4:
                return
            else:
                print("Invalid choice!")
        except ValueError:
            print("Invalid input!")
    
    def remove_from_favorites_interface(self, favorite_books: List[Dict]):
        """Interface to remove books from favorites"""
        try:
            book_id = int(input("Enter book ID to remove from favorites: "))
            book = next((b for b in favorite_books if b['book_id'] == book_id), None)
            
            if not book:
                print("Book ID not found in your favorites!")
                return
            
            confirm = input(f"Remove '{book['title']}' from favorites? (y/n): ").lower()
            if confirm == 'y':
                self.remove_from_favorites(book_id)
            else:
                print("Removal cancelled.")
                
        except ValueError:
            print("Invalid book ID!")
    
    def search_within_favorites(self):
        """Search within favorite books"""
        if not self.current_student.favorites:
            print("No favorite books to search!")
            return
        
        query = input("Search within your favorites: ").strip().lower()
        if not query:
            self.view_favorites()
            return
        
        matching_favorites = []
        for book_id in self.current_student.favorites:
            if book_id in self.books_data:
                book = self.books_data[book_id]
                if (query in book['title'].lower() or 
                    query in book['author'].lower() or 
                    query in book['category'].lower()):
                    matching_favorites.append(book)
        
        if matching_favorites:
            self.display_search_results(matching_favorites, f"Favorites matching '{query}'")
        else:
            print(f"No favorites found matching '{query}'")
    
    def get_student_profile(self) -> Dict:
        """Get current student's profile information"""
        if not self.current_student:
            return {}
        
        return {
            'student_id': self.current_student.student_id,
            'name': self.current_student.name,
            'email': self.current_student.email,
            'registration_date': self.current_student.registration_date,
            'borrowed_books_count': len(self.current_student.borrowed_books),
            'favorites_count': len(self.current_student.favorites)
        }
    
    def display_student_dashboard(self):
        """Display student dashboard with summary"""
        if not self.current_student:
            print("Please login first!")
            return
        
        profile = self.get_student_profile()
        
        print("\n" + "="*60)
        print("              STUDENT DASHBOARD")
        print("="*60)
        print(f"👤 Name: {profile['name']}")
        print(f"🆔 Student ID: {profile['student_id']}")
        if profile['email']:
            print(f"📧 Email: {profile['email']}")
        print(f"📅 Member since: {profile['registration_date'][:10]}")
        print(f"📚 Books borrowed: {profile['borrowed_books_count']}")
        print(f"❤️  Favorite books: {profile['favorites_count']}")
        print("="*60)

def main():
    """Main function to demonstrate student functionality"""
    student_manager = StudentManager()
    
    while True:
        print("\n" + "="*50)
        print("         STUDENT LIBRARY SYSTEM")
        print("="*50)
        
        if not student_manager.current_student:
            print("1. Register as new student")
            print("2. Login")
            print("3. Exit")
            
            try:
                choice = int(input("\nSelect option: "))
                
                if choice == 1:
                    print("\n--- Student Registration ---")
                    student_id = input("Enter desired Student ID: ").strip()
                    name = input("Enter your full name: ").strip()
                    email = input("Enter email (optional): ").strip()
                    student_manager.register_student(student_id, name, email)
                
                elif choice == 2:
                    print("\n--- Student Login ---")
                    student_id = input("Enter your Student ID: ").strip()
                    student_manager.login_student(student_id)
                
                elif choice == 3:
                    print("Thank you for using the Student Library System!")
                    break
                
                else:
                    print("Invalid choice!")
                    
            except ValueError:
                print("Invalid input! Please enter a number.")
        
        else:
            # Student is logged in
            student_manager.display_student_dashboard()
            print("\n📚 What would you like to do?")
            print("1. Browse Categories")
            print("2. Search Books")
            print("3. View My Favorites")
            print("4. Logout")
            
            try:
                choice = int(input("\nSelect option: "))
                
                if choice == 1:
                    student_manager.browse_categories()
                elif choice == 2:
                    student_manager.search_interface()
                elif choice == 3:
                    student_manager.view_favorites()
                elif choice == 4:
                    student_manager.logout_student()
                else:
                    print("Invalid choice!")
                    
            except ValueError:
                print("Invalid input! Please enter a number.")
            except KeyboardInterrupt:
                print("\n\nLogging out...")
                student_manager.logout_student()
                break

if __name__ == "__main__":
    main()
