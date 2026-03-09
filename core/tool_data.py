# File: core/tool_data.py
# Update: 09/03/2026
# Lokesh-Kumar
import json
import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
JSON_FILE = os.path.join(BASE_DIR, 'core', 'data.json')

# >> Master map to merge overlapping categories
CATEGORY_MAPPING = {
    "ddos": "stress_testing",
    "bruteforce": "password_attack",
    "bruteforce_&_password_attacks": "password_attack",
    "termux_utilities_&_add_ons": "termux_utilities",
    "termux_utilities_&_add-ons": "termux_utilities",
    "osint_&_information_retrieval": "information_gathering",
    "social_engineering_&_phishing": "social_engineering",
    "linux_&_desktop_installation": "os_installation"
}

def clean_category_name(cat_name):
    if not cat_name: return "uncategorized"
    cat_name = str(cat_name).lower().replace(" ", "_")
    return CATEGORY_MAPPING.get(cat_name, cat_name)

def load_data():
    if not os.path.exists(JSON_FILE):
        print(f"[!] Error: {JSON_FILE} not found! Please check.")
        sys.exit(1)
        
    try:
        with open(JSON_FILE, 'r', encoding='utf-8') as f:
            raw_tools = json.load(f)
            
        categories_set = set()
        organized_tools = {}

        for tool_key, tool_info in raw_tools.items():
            cats = tool_info.get("category", [])
            if cats == [None] or not cats:
                cats = ["uncategorized"]

            for c in cats:
                clean_cat = clean_category_name(c)
                categories_set.add(clean_cat)
                
                if clean_cat not in organized_tools:
                    organized_tools[clean_cat] = {}
                organized_tools[clean_cat][tool_key] = tool_info

        category_map = {}
        for idx, cat_name in enumerate(sorted(categories_set), 1):
            category_map[str(idx).zfill(2)] = cat_name

        return raw_tools, organized_tools, category_map

    except Exception as e:
        print(f"[!] Error loading data: {e}")
        sys.exit(1)

RAW_TOOLS, TOOLS_BY_CATEGORY, TOOL_CATEGORIES = load_data()
