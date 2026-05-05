import json
import os
import sys

def _get_app_dir():
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.abspath(__file__))

VAR_FILE = os.path.join(_get_app_dir(), "variables.json")

def load_vars():
    if not os.path.exists(VAR_FILE):
        return {}
    try:
        with open(VAR_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading {VAR_FILE}: {e}")
        return {}

def save_vars(data):
    try:
        with open(VAR_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4)
    except Exception as e:
        print(f"Error saving {VAR_FILE}: {e}")

def get_var(name, default=""):
    data = load_vars()
    return data.get(name, default)

def set_var(name, value):
    data = load_vars()
    data[name] = value
    save_vars(data)
