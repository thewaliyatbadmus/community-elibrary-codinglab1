#!/usr/bin/env python3

from storage import load_books, save_books, load_users, save_users

def admin_menu():
    while True:
        print("\n--- Admin Dashboard ---")
        print("1. Add New Resource")
        print("2. Edit Existing Resource")
        print("3. Manage Users")
        print("4. Logout")

        choice = input("Enter your choice: ")

        if choice == "1":
            add_new_resource()
        elif choice == "2":
            edit_existing_resource()
        elif choice == "3":
            manage_users()
        elif choice == "4":
            print("Logging out...")
            break
        else:
            print("Invalid choice. Please try again.")

def add_new_resource():
    print("\n--- Add New Resource ---")
    title = input("Enter Title: ")
    author = input("Enter Author: ")
    subject = input("Enter Subject: ")
    language = input("Enter Language: ")
    file_path = input("Enter File Path or Link: ")

    # Load current books
    books = load_books()

    new_book = {
        "title": title,
        "author": author,
        "subject": subject,
        "language": language,
        "file": file_path
    }

    books.append(new_book)
    save_books(books)
    print(f"Resource '{title}' added successfully.")

def edit_existing_resource():
    print("\n--- Edit Existing Resource ---")
    books = load_books()
    if not books:
        print("No resources found.")
        return

    for idx, book in enumerate(books):
        print(f"{idx + 1}. {book['title']} by {book['author']}")

    choice = input("Select resource number to edit: ")
    if not choice.isdigit() or int(choice) < 1 or int(choice) > len(books):
        print("Invalid selection.")
        return

    idx = int(choice) - 1
    book = books[idx]

    print(f"Editing '{book['title']}'")
    book['title'] = input(f"Title [{book['title']}]: ") or book['title']
    book['author'] = input(f"Author [{book['author']}]: ") or book['author']
    book['subject'] = input(f"Subject [{book['subject']}]: ") or book['subject']
    book['language'] = input(f"Language [{book['language']}]: ") or book['language']
    book['file'] = input(f"File Path [{book['file']}]: ") or book['file']

    save_books(books)
    print(f"Resource '{book['title']}' updated successfully.")

def manage_users():
    print("\n--- Manage Users ---")
    users = load_users()

    print("1. View Users")
    print("2. Add User")
    print("3. Remove User")

    choice = input("Select an option: ")
    if choice == "1":
        if not users:
            print("No users found.")
            return
        for idx, user in enumerate(users):
            print(f"{idx + 1}. {user['username']}")
    elif choice == "2":
        username = input("Enter new username: ")
        new_user = {"username": username}
        users.append(new_user)
        save_users(users)
        print(f"User '{username}' added successfully.")
    elif choice == "3":
        if not users:
            print("No users to remove.")
            return
        for idx, user in enumerate(users):
            print(f"{idx + 1}. {user['username']}")
        choice = input("Select user number to remove: ")
        if not choice.isdigit() or int(choice) < 1 or int(choice) > len(users):
            print("Invalid selection.")
            return
        removed_user = users.pop(int(choice) - 1)
        save_users(users)
        print(f"User '{removed_user['username']}' removed successfully.")
    else:
        print("Invalid option.")

# For direct testing (optional)
if __name__ == "__main__":
    admin_menu()
