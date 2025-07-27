import storage

# --- Step 1: Test adding a resource ---
test_resource = {
    "id": "book101",
    "title": "Python for Beginners",
    "author": "John Doe",
    "subject": "Programming",
    "language": "English",
    "filepath": "resources/python_beginners.pdf"
}
storage.add_resource(test_resource)
print("✅ Resource added.")

# --- Step 2: Test adding a user ---
test_user = {
    "username": "testuser",
    "password": "pass123",
    "favorites": []
}
storage.add_user(test_user)
print("✅ User added.")

# --- Step 3: Test logging usage ---
storage.log_usage("book101", "view")
storage.log_usage("book101", "download")
print("✅ Usage logged.")

# --- Step 4: Load and print everything ---
print("\n--- Resources ---")
print(storage.load_resources())

print("\n--- Users ---")
print(storage.load_users())

print("\n--- Usage Logs ---")
print(storage.load_usage())