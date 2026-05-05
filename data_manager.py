import json
import os
import sys
import uuid

def _get_app_dir():
    """Return the directory where the app lives, works for both script and frozen EXE."""
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.abspath(__file__))

DATA_FILE = os.path.join(_get_app_dir(), "hotkeys.json")

def load_data():
    if not os.path.exists(DATA_FILE):
        return {"hotkeys": []}
    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading {DATA_FILE}: {e}")
        return {"hotkeys": []}

def save_data(data):
    try:
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4)
    except Exception as e:
        print(f"Error saving {DATA_FILE}: {e}")

def get_all_hotkeys():
    data = load_data()
    return data.get("hotkeys", [])

def add_hotkey(keys, label, content):
    data = load_data()
    
    # Check for duplicate keys
    for hk in data.get("hotkeys", []):
        if hk["keys"].lower() == keys.lower():
            raise ValueError(f"Hotkey '{keys}' is already in use.")
            
    new_hk = {
        "id": str(uuid.uuid4()),
        "keys": keys,
        "label": label,
        "content": content
    }
    data["hotkeys"].append(new_hk)
    save_data(data)
    return new_hk

def update_hotkey(hk_id, keys, label, content):
    data = load_data()
    
    # Check if duplicate exists among other items
    for hk in data.get("hotkeys", []):
        if hk["id"] != hk_id and hk["keys"].lower() == keys.lower():
            raise ValueError(f"Hotkey '{keys}' is already in use.")
            
    for hk in data.get("hotkeys", []):
        if hk["id"] == hk_id:
            hk["keys"] = keys
            hk["label"] = label
            hk["content"] = content
            save_data(data)
            return hk
            
    raise ValueError("Hotkey not found.")

def delete_hotkey(hk_id):
    data = load_data()
    hotkeys = data.get("hotkeys", [])
    data["hotkeys"] = [hk for hk in hotkeys if hk["id"] != hk_id]
    save_data(data)
