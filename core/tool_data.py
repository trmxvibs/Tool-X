# File: core/tool_data.py
# Update:12/04/2026 
# Developer: Lokesh-Kumar 
import json
import os
import sys
from rich.console import Console
from rich.panel import Panel

console = Console()

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
        console.print(f"\n[bold red][!] CRITICAL ERROR:[/] [yellow]{JSON_FILE}[/] not found!")
        console.print("[cyan]Tip: Make sure data.json exists in the core folder.[/]")
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

    except json.JSONDecodeError as e:
        err_msg = f"[bold red]Fatal Error: data.json ka format corrupt hai![/]\n\n[yellow]Technical Details:[/] {e}\n[cyan]Tip: Check karein ki file me koi extra comma (,) ya missing bracket toh nahi hai.[/]"
        console.print(Panel(err_msg, title="[bold red]JSON Parsing Error[/]", border_style="red"))
        sys.exit(1)
    except Exception as e:
        console.print(f"[bold red][!] Unexpected Error loading data:[/] {e}")
        sys.exit(1)

# Initialize variables securely
RAW_TOOLS, TOOLS_BY_CATEGORY, TOOL_CATEGORIES = load_data()
