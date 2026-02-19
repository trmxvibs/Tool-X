# File: core/tool_data.py
# Update: 19/02/2026
import json
import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
JSON_FILE = os.path.join(BASE_DIR, 'core', 'tools.json')

def load_data():
    if not os.path.exists(JSON_FILE):
        print(f"Error: {JSON_FILE} not found!")
        sys.exit(1)
        
    try:
        with open(JSON_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data.get('tools', {}), data.get('categories', {})
    except json.JSONDecodeError as e:
        print(f"Error: tools.json is corrupted or has syntax error.\nDetails: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected Error loading data: {e}")
        sys.exit(1)

TOOLS, TOOL_CATEGORIES = load_data()
