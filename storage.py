import json
import os
# Define file paths
DATA_DIR = 'data'
RESOURCES_FILE = os.path.join(DATA_DIR, 'resources.json')
USERS_FILE = os.path.join(DATA_DIR, 'users.json')
USAGE_FILE = os.path.join(DATA_DIR, 'usage.json')

# Ensure data directory exists
os.makedirs(DATA_DIR, exist_ok=True)

# ---------- Helper Functions ----------

def load_json(filepath):
    if not os.path.exists(filepath):
        return []
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_json(filepath, data):
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4)

# ---------- Resource Functions ----------

def load_resources():
    return load_json(RESOURCES_FILE)

def save_resources(resources):
    save_json(RESOURCES_FILE, resources)

def add_resource(resource):
    resources = load_resources()
    resources.append(resource)
    save_resources(resources)

# ---------- User Functions ----------

def load_users():
    return load_json(USERS_FILE)

def save_users(users):
    save_json(USERS_FILE, users)

def add_user(user):
    users = load_users()
    users.append(user)
    save_users(users)

# ---------- Usage Log Functions ----------

def load_usage():
    return load_json(USAGE_FILE)

def save_usage(logs):
    save_json(USAGE_FILE, logs)

def log_usage(resource_id, action):  # action = 'view' or 'download'
    logs = load_usage()
    for log in logs:
        if log['resource_id'] == resource_id:
            log[action] += 1
            save_usage(logs)
            return
    # If new entry
    logs.append({'resource_id': resource_id, 'view': 0, 'download': 0})
    logs[-1][action] = 1
    save_usage(logs)
