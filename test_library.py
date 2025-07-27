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
    with open(filename, "w") as f
