import os
import json
import getpass

# --- Data Storage Files ---
USERS_FILE = "users.json"
BOOKS_FILE = "books.json"
USAGE_FILE = "usage.json"

# --- Helper Functions ---

def load_data(filename, default):
    if not os.path.exists(filename):
        with open(filename, "w") as f:
            json.dump(default, f)
    with open(filename, "r") as f:
        return json.load(f)

def save_data(filename, data):
    with open(filename, "w") as f:
        json.dump(data, f, indent=2)

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def pause():
    input("\nPress Enter to continue...")

# --- Data Initialization ---

users = load_data(USERS_FILE, [{"username": "admin", "password": "admin", "role": "admin"}])
books = load_data(BOOKS_FILE, [])
usage = load_data(USAGE_FILE, {})

# --- Authentication ---

def register_user():
    clear_screen()
    print("*** Student Registration ***")
    username = input("Choose a username: ").strip()
    if any(u["username"] == username for u in users):
        print("Username already exists.")
        pause()
        return None
    password = getpass.getpass("Choose a password: ")
    users.append({"username": username, "password": password, "role": "student", "favorites": [], "history": []})
    save_data(USERS_FILE, users)
    print("Registration successful!")
    pause()
    return username

def login(role="student"):
    clear_screen()
    print(f"*** {role.capitalize()} Login ***")
    username = input("Username: ").strip()
    password = getpass.getpass("Password: ")
    for u in users:
        if u["username"] == username and u["password"] == password and u["role"] == role:
            print("Login successful!")
            pause()
            return username
    print("Invalid credentials.")
    pause()
    return None

def get_user(username):
    for u in users:
        if u["username"] == username:
            return u
    return None

# --- Book Management ---

def add_book():
    clear_screen()
    print("*** Add New Resource ***")
    title = input("Title: ").strip()
    author = input("Author: ").strip()
    subject = input("Subject: ").strip()
    language = input("Language: ").strip()
    file_path = input("File path (PDF/TXT): ").strip()
    category = input("Category (Core Subjects/Local Storybooks/Study Skills): ").strip()
    book = {
        "id": len(books) + 1,
        "title": title,
        "author": author,
        "subject": subject,
        "language": language,
        "file_path": file_path,
        "category": category
    }
    books.append(book)
    save_data(BOOKS_FILE, books)
    print("Resource added successfully!")
    pause()

def edit_book():
    clear_screen()
    print("*** Edit Existing Resource ***")
    list_books()
    try:
        idx = int(input("Enter book ID to edit: ")) - 1
        if idx < 0 or idx >= len(books):
            print("Invalid ID.")
            pause()
            return
        book = books[idx]
        print(f"Editing: {book['title']}")
        book['title'] = input(f"Title [{book['title']}]: ") or book['title']
        book['author'] = input(f"Author [{book['author']}]: ") or book['author']
        book['subject'] = input(f"Subject [{book['subject']}]: ") or book['subject']
        book['language'] = input(f"Language [{book['language']}]: ") or book['language']
        book['file_path'] = input(f"File path [{book['file_path']}]: ") or book['file_path']
        book['category'] = input(f"Category [{book['category']}]: ") or book['category']
        save_data(BOOKS_FILE, books)
        print("Resource updated!")
    except ValueError:
        print("Invalid input.")
    pause()

def list_books(filter_func=None):
    print("\nAvailable Books:")
    filtered = [b for b in books if filter_func is None or filter_func(b)]
    if not filtered:
        print("No books found.")
        return []
    for b in filtered:
        print(f"{b['id']}. {b['title']} | {b['author']} | {b['subject']} | {b['language']} | {b['category']}")
    return filtered

def search_books():
    clear_screen()
    print("*** Search Library ***")
    keyword = input("Enter keyword (title, author, subject): ").lower()
    results = [b for b in books if keyword in b['title'].lower() or keyword in b['author'].lower() or keyword in b['subject'].lower()]
    if not results:
        print("No matching books found.")
        pause()
        return None
    for b in results:
        print(f"{b['id']}. {b['title']} | {b['author']} | {b['subject']} | {b['language']} | {b['category']}")
    try:
        book_id = int(input("Enter book ID to select (0 to cancel): "))
        if book_id == 0:
            return None
        return next((b for b in books if b['id'] == book_id), None)
    except ValueError:
        return None

def browse_categories():
    clear_screen()
    print("*** Browse Categories ***")
    categories = set(b['category'] for b in books)
    if not categories:
        print("No categories available.")
        pause()
        return None
    for i, cat in enumerate(categories, 1):
        print(f"{i}. {cat}")
    try:
        choice = int(input("Select category (0 to cancel): "))
        if choice == 0:
            return None
        selected = list(categories)[choice - 1]
        filtered = [b for b in books if b['category'] == selected]
        for b in filtered:
            print(f"{b['id']}. {b['title']} | {b['author']} | {b['subject']} | {b['language']}")
        book_id = int(input("Enter book ID to select (0 to cancel): "))
        if book_id == 0:
            return None
        return next((b for b in books if b['id'] == book_id), None)
    except (ValueError, IndexError):
        return None

# --- Book Actions ---

def book_actions(book, user):
    while True:
        clear_screen()
        print(f"*** {book['title']} by {book['author']} ***")
        print("1. View Online")
        print("2. Download File")
        print("3. Add to Favorites")
        print("4. Return to Library")
        choice = input("Choose an action: ")
        if choice == "1":
            view_book(book)
            record_usage(book, "view")
            if user:
                user['history'].append(book['id'])
                save_data(USERS_FILE, users)
        elif choice == "2":
            download_book(book)
            record_usage(book, "download")
            if user:
                user['history'].append(book['id'])
                save_data(USERS_FILE, users)
        elif choice == "3" and user:
            if book['id'] not in user['favorites']:
                user['favorites'].append(book['id'])
                save_data(USERS_FILE, users)
                print("Added to favorites!")
            else:
                print("Already in favorites.")
            pause()
        elif choice == "4":
            break
        else:
            print("Invalid choice.")
            pause()

def view_book(book):
    clear_screen()
    print(f"*** Viewing: {book['title']} ***")
    if os.path.exists(book['file_path']):
        with open(book['file_path'], "r", encoding="utf-8", errors="ignore") as f:
            print(f.read(1000))  # Show first 1000 chars
    else:
        print("File not found.")
    pause()

def download_book(book):
    clear_screen()
    print(f"*** Download: {book['title']} ***")
    if os.path.exists(book['file_path']):
        dest = input("Enter destination filename: ").strip()
        with open(book['file_path'], "rb") as src, open(dest, "wb") as dst:
            dst.write(src.read())
        print(f"Downloaded to {dest}")
    else:
        print("File not found.")
    pause()

def record_usage(book, action):
    usage.setdefault(str(book['id']), {"views": 0, "downloads": 0})
    if action == "view":
        usage[str(book['id'])]["views"] += 1
    elif action == "download":
        usage[str(book['id'])]["downloads"] += 1
    save_data(USAGE_FILE, usage)
