# File: tool-x.py
# Lokesh Kumar
# Date 08/11/2025
# Github : https://github.com/trmxvibs
# Author : Lokesh kumar
# File: tool-x.py
import os
import sys
script_dir = os.path.dirname(os.path.abspath(__file__))


os.chdir(script_dir)

from time import sleep as timeout
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True) 

# --- Import Core Modules ---
# Check for core file existence after changing directory
if not os.path.exists('core/tool_data.py'):
    print(Fore.RED + "[!] ERROR: 'core/tool_data.py' not found." + Style.RESET_ALL)
    print(Fore.YELLOW + "    Please ensure the file structure is correct (core/tool_data.py exists)." + Style.RESET_ALL)
    sys.exit(1)

# Now perform the imports
from core.tool_data import TOOLS, TOOL_CATEGORIES
from core.installation_logic import install_github_tool, install_termux_package, LOG_FILE, INSTALLED_TOOLS_FILE


# --- Utility Functions (Defined Locally) ---

def restart_program():
    """Restarts the script from the main menu by re-executing the Python interpreter."""
    python = sys.executable
    os.execl(python, python, *sys.argv)

def banner():
    """Displays the dynamic colored figlet banner for Tool-X."""
    os.system("clear")
    os.system("figlet Tool-X | lolcat -a -d 10")
    print(Fore.GREEN + Style.BRIGHT + "       -- Lokesh Kumar --" + Style.RESET_ALL)
    print("--------------------------------------------------")

# Define constants for the self-uninstaller
TOOL_DIR = os.path.expanduser("~/tool-x")
INSTALLER_SCRIPT = "tool-x.py"
BASHRC = os.path.join(os.environ.get('PREFIX', '/data/data/com.termux/files/usr'), 'etc/bash.bashrc')
ALIAS_NAME = "toolx"

# --- Installation Logic ---

def run_installation_batch(user_input, category_id):
    """Processes user input for multiple tool installations."""
    tools_to_install = user_input.split()
    category_tools = TOOLS.get(category_id, {})
    
    for tool_choice in tools_to_install:
        choice = tool_choice.strip().zfill(2)
        
        if choice == "00":
            return # Exit submenu
        
        if choice in category_tools:
            # Pass the tool_id (choice) and category_id to the core installer
            install_github_tool(choice, category_id)
        else:
            print(Fore.RED + f"\nERROR: Invalid tool number: {choice}" + Style.RESET_ALL)
            timeout(1)

    if tools_to_install:
        restart_program()
    else:
        restart_program()


# --- Special Menu Functions ---

def view_status_menu():
    """Displays the installation status dashboard."""
    banner()
    print(Fore.BLUE + Style.BRIGHT + "--- 📊 INSTALLATION STATUS DASHBOARD ---" + Style.RESET_ALL)

    # 1. Total Installed Tools
    installed_count = 0
    installed_tools = []
    if os.path.exists(INSTALLED_TOOLS_FILE):
        with open(INSTALLED_TOOLS_FILE, 'r') as f:
            lines = f.readlines()
            for line in lines:
                if line.strip():
                    installed_tools.append(line.split(':', 1))
            installed_count = len(installed_tools)

    print(Fore.CYAN + f"\n[+] Total Installed Tools: {Fore.GREEN}{installed_count}{Style.RESET_ALL}")
    
    if installed_count > 0:
        print(Fore.WHITE + "\n--- Installed List (Name : Path) ---" + Style.RESET_ALL)
        for name, path in installed_tools:
            print(f"  {Fore.GREEN}✓{Style.RESET_ALL} {name.ljust(20)} : {path.strip()}")
    else:
        print(Fore.YELLOW + "  (No successful tool installations tracked yet.)" + Style.RESET_ALL)

    # 2. Error Log Status
    print(Fore.RED + "\n--- Error Log Status ---" + Style.RESET_ALL)
    if os.path.exists(LOG_FILE) and os.stat(LOG_FILE).st_size > 0:
        print(Fore.YELLOW + f"  [!] Errors found in log file: {LOG_FILE}" + Style.RESET_ALL)
        print(Fore.YELLOW + "  [!] Last 5 Log Entries:" + Style.RESET_ALL)
        with open(LOG_FILE, 'r') as f:
            log_entries = f.readlines()
            for entry in log_entries[-5:]:
                print(Fore.RED + f"    {entry.strip()}" + Style.RESET_ALL)
    else:
        print(Fore.GREEN + "  [+] No errors logged yet." + Style.RESET_ALL)

    input(Fore.YELLOW + "\n[!] Press ENTER to return to the main menu..." + Style.RESET_ALL)
    restart_program()


def search_tool_menu():
    """Allows searching for tools by keyword."""
    banner()
    search_term = input(Fore.YELLOW + "Tool-X > Search > Enter keyword: " + Fore.WHITE).strip().lower()

    if not search_term:
        restart_program()
        return

    found_tools = []
    
    for cat_id, cat_tools in TOOLS.items():
        for tool_id, data in cat_tools.items():
            # Search in tool name and description
            if search_term in data['name'].lower() or search_term in data['desc'].lower():
                found_tools.append((cat_id, tool_id, data))

    banner()
    if found_tools:
        print(Fore.GREEN + f"[*] Found {len(found_tools)} tools matching '{search_term}':" + Style.RESET_ALL)
        
        search_map = {}
        for idx, (cat_id, tool_id, data) in enumerate(found_tools):
            display_id = str(idx + 1).zfill(2)
            print(f"    {Fore.CYAN}[{display_id}]{Style.RESET_ALL} {data['name']} (Cat: {cat_id}) - {data['desc']}")
            search_map[display_id] = (tool_id, cat_id) 
            
        print(Fore.YELLOW + "\n    [00] Back to main menu\n" + Style.RESET_ALL)
        
        user_input = input(Fore.YELLOW + "Tool-X > Search > set_install " + Fore.WHITE).split()
        
        for choice in user_input:
            choice = choice.strip().zfill(2)
            if choice == "00":
                restart_program()
                return
            
            if choice in search_map:
                tool_id_to_install, cat_id_to_install = search_map[choice]
                install_github_tool(tool_id_to_install, cat_id_to_install)
            else:
                 print(Fore.RED + f"\nERROR: Invalid tool number: {choice}" + Style.RESET_ALL)
                 timeout(1)
        
        if user_input:
            restart_program()
            
    else:
        print(Fore.RED + f"\n[!] No tools found matching '{search_term}'." + Style.RESET_ALL)
        timeout(2)
        restart_program()


def uninstall_tool_menu():
    """Displays list of installed tools and allows uninstallation."""
    
    if not os.path.exists(INSTALLED_TOOLS_FILE) or os.stat(INSTALLED_TOOLS_FILE).st_size == 0:
        banner()
        print(Fore.YELLOW + "[!] No tools tracked yet. Install some tools first." + Style.RESET_ALL)
        timeout(2)
        restart_program()
        return

    with open(INSTALLED_TOOLS_FILE, 'r') as f:
        lines = f.readlines()

    installed_map = {}
    
    banner()
    print(Fore.RED + "--- 🗑️ Uninstall Installed Tools ---" + Style.RESET_ALL)
    
    for idx, line in enumerate(lines):
        try:
            tool_name, tool_path = line.strip().split(':', 1)
            display_id = str(idx + 1).zfill(2)
            print(f"    {Fore.CYAN}[{display_id}]{Style.RESET_ALL} {tool_name} (Path: {tool_path})")
            installed_map[display_id] = {'name': tool_name, 'path': tool_path, 'line': line}
        except ValueError:
            continue
            
    if not installed_map:
        print(Fore.YELLOW + "[!] Installed file is corrupted or empty." + Style.RESET_ALL)
        timeout(2)
        restart_program()
        return

    print(Fore.YELLOW + "\n    [00] Back to main menu\n" + Style.RESET_ALL)
    
    user_input = input(Fore.RED + "Tool-X > Uninstall > Select tool number(s) to remove: " + Fore.WHITE).split()
    
    tools_to_remove = []
    
    for choice in user_input:
        choice = choice.strip().zfill(2)
        if choice == "00":
            restart_program()
            return
        
        if choice in installed_map:
            tools_to_remove.append(installed_map[choice])
        else:
            print(Fore.RED + f"\nERROR: Invalid tool number: {choice}" + Style.RESET_ALL)
            timeout(1)

    if tools_to_remove:
        for tool in tools_to_remove:
            print(Fore.RED + f"[*] Removing {tool['name']} at {tool['path']}..." + Style.RESET_ALL)
            # Remove the directory
            os.system(f"rm -rf {tool['path']}")
            print(Fore.GREEN + f"[+] {tool['name']} removed successfully." + Style.RESET_ALL)
            
            # Remove the entry from the tracking file
            lines.remove(tool['line'])

        # Rewrite the tracking file without the removed entries
        with open(INSTALLED_TOOLS_FILE, 'w') as f:
            f.writelines(lines)
            
        print(Fore.GREEN + "\n[+] Uninstallation complete." + Style.RESET_ALL)
        timeout(2)
    
    restart_program()


def uninstall_self_menu():
    """Removes the alias and the entire Tool-X directory (Self-Destruct)."""
    banner()
    print(Fore.RED + Style.BRIGHT + "--- ⚠️ SELF-DESTRUCT SEQUENCE INITIATED ⚠️ ---" + Style.RESET_ALL)
    print(Fore.YELLOW + f"[*] This will permanently remove the alias '{ALIAS_NAME}' and the directory '{TOOL_DIR}'." + Style.RESET_ALL)
    
    confirm = input(Fore.RED + Style.BRIGHT + "[?] Are you absolutely sure you want to proceed? (yes/NO): " + Fore.WHITE).strip()

    if confirm.lower() != 'yes':
        print(Fore.GREEN + "\n[*] Uninstallation cancelled." + Style.RESET_ALL)
        timeout(2)
        restart_program()
        return

    # 1. Remove Alias (User is informed as external script setup is pending)
    print(Fore.YELLOW + "[*] If you used a setup script, you may need to manually remove the alias line containing 'toolx' from your bash.bashrc." + Style.RESET_ALL)

    # 2. Remove the Tool Directory
    try:
        os.system(f"rm -rf {TOOL_DIR}")
        print(Fore.GREEN + f"[+] Directory '{TOOL_DIR}' removed successfully." + Style.RESET_ALL)
    except Exception as e:
        print(Fore.RED + f"[!] Failed to remove directory: {e}" + Style.RESET_ALL)

    print(Fore.RED + Style.BRIGHT + "\n\n[!] Tool-X has been completely removed. Exiting." + Style.RESET_ALL)
    sys.exit(0)


# --- Sub Menu Definitions ---

def submenu(category_id):
    """Displays and handles logic for a specific category submenu."""
    banner()
    
    category_name = TOOL_CATEGORIES.get(category_id, "Unknown Category")
    print(Fore.BLUE + Style.BRIGHT + f"--- 🛠️ Category {category_id}: {category_name} ---" + Style.RESET_ALL)
    
    category_tools = TOOLS.get(category_id, {})
    
    for tool_id, data in category_tools.items():
        formatted_id = str(tool_id).zfill(2)
        tool_name = data['name']
        tool_desc = data['desc']
        help_cmd = data.get('help_cmd', '')
        
        if help_cmd:
            display_cmd = f" | RUN: {Fore.YELLOW}{help_cmd.split()[0]}...{Style.RESET_ALL}"
        else:
            display_cmd = ""
            
        print(f"    {Fore.GREEN}[{formatted_id}]{Style.RESET_ALL} {tool_name}: {tool_desc}{display_cmd}")
    
    print(Fore.YELLOW + "\n    [00] Back to main menu\n" + Style.RESET_ALL)
    
    user_input = input(Fore.YELLOW + f"Tool-X > {category_name.split()[0]} > set_install " + Fore.WHITE)
    
    run_installation_batch(user_input, category_id)

def main_menu():
    """Displays the main category menu."""
    banner()
    
    for cid, cname in TOOL_CATEGORIES.items():
        print(f"   {Fore.CYAN}[{cid}]{Style.RESET_ALL} {cname}")

    print(Fore.YELLOW + "\n   [94] View Installation Status" + Style.RESET_ALL) # STATUS MENU
    print(Fore.YELLOW + "   [97] Search Tool (by keyword)" + Style.RESET_ALL)
    print(Fore.RED + "   [98] Uninstall Tools" + Style.RESET_ALL)
    print(Fore.BLUE + "   [99] Update the Framework" + Style.RESET_ALL)
    print(Fore.MAGENTA + "   [96] Uninstall Tool-X Framework (Self-Destruct)" + Style.RESET_ALL)
    print(Fore.RED + "   [00] Exit the Framework\n" + Style.RESET_ALL)
    
    main_choice = input(Fore.YELLOW + "Tool-X > set_install " + Fore.WHITE).strip().zfill(2)

    if main_choice in TOOL_CATEGORIES:
        submenu(main_choice)
    elif main_choice == "94":
        view_status_menu()
    elif main_choice == "97":
        search_tool_menu()
    elif main_choice == "98":
        uninstall_tool_menu()
    elif main_choice == "99":
        print(Fore.CYAN + "\n[*] Fetching latest updates from Git..." + Style.RESET_ALL)
        os.system("git pull")
        restart_program()
    elif main_choice == "96":
        uninstall_self_menu()
    elif main_choice == "00":
        print(Fore.GREEN + "\n[+] Exiting. Thank you for using Tool-X Installer!" + Style.RESET_ALL)
        sys.exit(0)
    else:
        print(Fore.RED + "\nERROR: Wrong Input" + Style.RESET_ALL);timeout(1);restart_program()


if __name__ == "__main__":
    try:
        # Final dependency check for colorama and figlet/lolcat
        try:
            import colorama
            if os.system("which figlet > /dev/null 2>&1") != 0 or os.system("which lolcat > /dev/null 2>&1") != 0:
                 print(Fore.RED + "--------------------------------------------------------" + Style.RESET_ALL)
                 print(Fore.RED + Style.BRIGHT + "[!] DISPLAY DEPENDENCY ERROR:" + Style.RESET_ALL)
                 print(Fore.YELLOW + "    The Tool-X script requires 'figlet' and 'lolcat' for the banner." + Style.RESET_ALL)
                 print(Fore.YELLOW + "    Please run: " + Fore.GREEN + "$ pkg install figlet lolcat -y" + Style.RESET_ALL)
                 print(Fore.RED + "--------------------------------------------------------" + Style.RESET_ALL)
                 sys.exit(1)
        except ImportError:
            print(Fore.RED + "--------------------------------------------------------" + Style.RESET_ALL)
            print(Fore.RED + Style.BRIGHT + "[!] DEPENDENCY ERROR:" + Style.RESET_ALL)
            print(Fore.YELLOW + "    The Tool-X script requires the 'colorama' library." + Style.RESET_ALL)
            print(Fore.YELLOW + "    Please run the following command and try again:" + Fore.GREEN + " $ pip install colorama" + Style.RESET_ALL)
            print(Fore.RED + "--------------------------------------------------------" + Style.RESET_ALL)
            sys.exit(1)
            
        main_menu()
    except KeyboardInterrupt:
        print(Fore.RED + "\n[!] Program stopped by user. Exiting..." + Style.RESET_ALL)
        sys.exit(0)
