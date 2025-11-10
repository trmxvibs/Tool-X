# File: core/installation_logic.py
# Date : 08/11/2025
# Github : https://github.com/trmxvibs
# Author : Lokesh kumar
import os
import time
import sys
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

# Import tool definitions and data
from core.tool_data import TOOLS 

# Define log file path and track installed tools
LOG_FILE = os.path.expanduser("~/tool-x_error.log")
INSTALLED_TOOLS_FILE = os.path.expanduser("~/tool-x_installed.txt")

# --- Logging & Tracking Utilities ---

def log_error(message):
    """Writes an error message to the log file."""
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a") as f:
        f.write(f"[{timestamp}] ERROR: {message}\n")

def track_installed_tool(tool_name, tool_dir):
    """Adds a newly installed tool and its path to the tracking file."""
    with open(INSTALLED_TOOLS_FILE, "a") as f:
        f.write(f"{tool_name}:{tool_dir}\n")

# --- Installation Utilities ---

# NOTE: mirror change is now handled by the external setup script.

def check_package_manager(pkg_manager):
    """Ensures pip, npm, or go is installed if required."""
    if pkg_manager == "python" or pkg_manager == "pip":
        install_termux_package("python")
        os.system("pip install --upgrade pip > /dev/null 2>&1")
    elif pkg_manager == "nodejs" or pkg_manager == "npm":
        install_termux_package("nodejs")
    elif pkg_manager == "go":
        install_termux_package("golang")

def display_tool_help(tool_name, tool_dir, help_cmd):
    """Displays instructions on how to run the installed tool."""
    print(Fore.BLUE + Style.BRIGHT + "\n\n--- 🚀 EXECUTION GUIDE ---" + Style.RESET_ALL)
    print(Fore.WHITE + f"Tool Name: {tool_name}")
    print(Fore.WHITE + f"Installation Path: ~/{os.path.basename(tool_dir)}")
    
    if help_cmd:
        print(Fore.CYAN + "\n[1] To RUN the tool, first change directory:" + Style.RESET_ALL)
        print(Fore.YELLOW + f"    cd {os.path.basename(tool_dir)}" + Style.RESET_ALL)
        print(Fore.CYAN + "\n[2] Then, check the help menu using the command:" + Style.RESET_ALL)
        print(Fore.GREEN + Style.BRIGHT + f"    {help_cmd}" + Style.RESET_ALL)
    else:
        print(Fore.YELLOW + "\n[!] Execution command not specified in tool data." + Style.RESET_ALL)
        print(Fore.YELLOW + "    Please 'cd' into the directory and check the README file." + Style.RESET_ALL)
    print(Fore.BLUE + "-----------------------------" + Style.RESET_ALL)
    time.sleep(2)


def handle_post_install(tool_name, tool_dir, help_cmd):
    """Asks the user whether to open the installed tool's directory, then displays help."""
    
    print(Fore.CYAN + Style.BRIGHT + "\n[?] Installation finished.")
    
    if os.path.isdir(tool_dir):
        track_installed_tool(tool_name, tool_dir) # Track successfully installed tool
        
        # Display help before asking to open
        display_tool_help(tool_name, tool_dir, help_cmd)

        choice = input(Fore.YELLOW + f"[?] Do you want to open the tool folder ({os.path.basename(tool_dir)}) now? (y/n): " + Style.RESET_ALL).strip().lower()
        
        if choice == 'y':
            print(Fore.GREEN + f"[*] Opening directory: {tool_dir}")
            os.execlp("bash", "bash", "-c", f"cd {tool_dir} && exec bash")

    print(Fore.WHITE + "[*] Returning to the main menu...")
    time.sleep(1) 
    return


def install_termux_package(package_name):
    """Installs an APT-based package."""
    print(Fore.CYAN + f"\n[+] Installing Termux package: {package_name}...")
    
    # Update and install
    os.system("pkg update -y") 
    install_status = os.system(f"pkg install {package_name} -y")
    
    if install_status != 0:
        log_error(f"Failed to install package: {package_name}. Exit code: {install_status}")
        print(Fore.RED + f"[!] ERROR: Failed to install package {package_name}. Check {LOG_FILE}" + Style.RESET_ALL)
    else:
        print(Fore.GREEN + f"[+] {package_name} installed successfully.")
    
    time.sleep(1)


def install_github_tool(tool_id, category_id):
    """Clones and installs a tool from its GitHub repository based on ID."""
    
    tool_data = TOOLS.get(category_id, {}).get(tool_id, {})
    if not tool_data:
        print(Fore.RED + f"\nERROR: Tool ID {tool_id} not found." + Style.RESET_ALL)
        return

    tool_name = tool_data["name"]
    repo_url = tool_data["repo"]
    req_packages = tool_data.get("reqs", "")
    install_command = tool_data.get("install_cmd", "")
    help_cmd = tool_data.get("help_cmd", "") # Get help command
    
    # Sanitized directory name
    tool_dir_name = tool_name.replace(' ', '_').replace('/', '_').replace('-', '_').replace('.', '_')
    tool_dir = os.path.expanduser(f"~/{tool_dir_name}")

    # 1. Install required dependencies and check package managers
    install_termux_package("git") # Ensure git is available
    if req_packages:
        print(Fore.YELLOW + f"[*] Installing dependencies: {req_packages}")
        for pkg in req_packages.split():
            # Check package manager dependencies (pip, npm, go)
            check_package_manager(pkg)
            # Install other dependencies
            if pkg not in ["python", "nodejs", "go", "pip", "npm"]:
                install_termux_package(pkg)

    # 2. Clone the repository
    print(Fore.CYAN + f"\n[+] Cloning {tool_name} from GitHub...")
    if os.path.exists(tool_dir):
        print(Fore.YELLOW + f"[*] Directory {tool_dir_name} already exists. Skipping cloning.")
    else:
        clone_status = os.system(f"git clone {repo_url} {tool_dir}")
        if clone_status != 0:
             log_error(f"Failed to clone {tool_name} ({repo_url}).")
             print(Fore.RED + f"[!] ERROR: Failed to clone {tool_name}. Check {LOG_FILE}" + Style.RESET_ALL)
             return

    # 3. Apply execute permissions (Crucial for shell scripts)
    os.system(f"chmod -R 777 {tool_dir}")

    # 4. Run custom installation command
    if install_command:
        print(Fore.CYAN + f"[*] Running custom installation steps for {tool_name}...")
        install_status = os.system(f"cd {tool_dir} && {install_command}")
        if install_status != 0:
             log_error(f"Failed to run install command for {tool_name}.")
             print(Fore.RED + f"[!] ERROR: Custom install failed for {tool_name}. Check {LOG_FILE}" + Style.RESET_ALL)
             return
    
    # 5. Handle post installation prompt and display help
    handle_post_install(tool_name, tool_dir, help_cmd)

# --- Define what is exported ---

__all__ = ['install_github_tool', 'install_termux_package', 'LOG_FILE', 'INSTALLED_TOOLS_FILE']
