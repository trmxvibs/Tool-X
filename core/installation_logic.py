# File: core/installation_logic.py
# Update:12/04/2026 
# Developer: Lokesh-kumar 
import os
import time
import subprocess
import shutil
import platform
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.panel import Panel
from rich.text import Text
from rich.prompt import Confirm

from core.tool_data import RAW_TOOLS

HOME_DIR = os.path.expanduser("~")

# >> CLEAN FOLDER
TOOLX_SYSTEM_DIR = os.path.join(HOME_DIR, ".tool-x")
if not os.path.exists(TOOLX_SYSTEM_DIR):
    os.makedirs(TOOLX_SYSTEM_DIR)

LOG_FILE = os.path.join(TOOLX_SYSTEM_DIR, "error.log")
INSTALLED_TOOLS_FILE = os.path.join(TOOLX_SYSTEM_DIR, "installed.json")

INSTALL_DEST_DIR = os.path.join(HOME_DIR, "ToolX_Installed_Tools") 
if not os.path.exists(INSTALL_DEST_DIR):
    os.makedirs(INSTALL_DEST_DIR)

console = Console()

# >> OS DETECTION 
def detect_os():
    """Smartly identifies the exact operating system environment"""
    sys_os = platform.system().lower()
    
    if sys_os == "windows":
        return "windows"
    elif "com.termux" in os.environ.get("PREFIX", "") or os.path.exists("/data/data/com.termux"):
        return "termux"
    elif sys_os == "darwin":
        return "macos"
    elif sys_os == "linux":
        return "linux" 
    return "other"

CURRENT_OS = detect_os()

# >> SMART PACKAGE MANAGER 
def get_install_command(pkg):
    """Returns the correct installation command as a secure LIST based on the OS"""
    if CURRENT_OS == "termux":
        return ["pkg", "install", "-y", pkg]
    elif CURRENT_OS == "macos":
        return ["brew", "install", pkg]
    elif CURRENT_OS == "windows":
        if shutil.which("choco"):
            return ["choco", "install", pkg, "-y"]
        elif shutil.which("winget"):
            return ["winget", "install", pkg, "-e", "--accept-package-agreements"]
        return None
    elif CURRENT_OS == "linux":
        if shutil.which("apt-get"):
            return ["sudo", "apt-get", "install", "-y", pkg]
        elif shutil.which("pacman"):
            return ["sudo", "pacman", "-S", "--noconfirm", pkg]
        elif shutil.which("dnf"):
            return ["sudo", "dnf", "install", "-y", pkg]
        elif shutil.which("yum"):
            return ["sudo", "yum", "install", "-y", pkg]
        else:
            return ["sudo", "apt-get", "install", "-y", pkg] 
    return None

def run_command(command_list, description, cwd=None):
    """Runs commands securely (shell=False) with a progress spinner"""
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True,
    ) as progress:
        progress.add_task(description=description, total=None)
        try:
            # shell=False is used automatically because we are passing a list. This is 100% secure.
            result = subprocess.run(
                command_list, shell=False, cwd=cwd, capture_output=True, text=True
            )
            if result.returncode != 0:
                timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
                with open(LOG_FILE, "a", encoding='utf-8') as f:
                    cmd_str = " ".join(command_list)
                    f.write(f"\n[{timestamp}] FAILED: {cmd_str}\nERROR: {result.stderr}\n")
                return False, result.stderr
            return True, result.stdout
        except Exception as e:
            return False, str(e)

def check_dependencies(deps_list):
    """Automatically checks and installs dependencies universally"""
    if not deps_list or deps_list == [None]: 
        return True
    
    for pkg in deps_list:
        if not pkg or pkg in ["bash", "cmd", "powershell"]: 
            continue

        if shutil.which(pkg): 
            continue
        
        console.print(f"[dim]Installing missing dependency: {pkg}...[/]")
        
        install_cmd = get_install_command(pkg)
        
        if install_cmd:
            success, _ = run_command(install_cmd, f"Installing {pkg}...")
            if not success:
                console.print(f"[bold red]Failed to install dependency: {pkg}[/]")
                if CURRENT_OS == "windows":
                     console.print(f"[yellow]  Try installing '{pkg}' manually on Windows.[/]")
                return False
        else:
            console.print(f"[yellow]Could not determine package manager for '{pkg}'. Install manually.[/]")
            
    return True

def install_tool(tool_key):
    """Main installation logic with Universal OS Compatibility Check & Secure Execution"""
    try:
        tool_data = RAW_TOOLS[tool_key]
    except KeyError:
        console.print("[bold red]Error: Tool not found.[/]")
        return

    tool_name = tool_data.get("name", tool_key)
    repo_url = tool_data.get("url")
    pkg_manager = tool_data.get("package_manager", "git")
    
    # >> UNIVERSAL OS COMPATIBILITY CHECK 
    supported_os = tool_data.get("os", ["linux", "termux", "windows", "macos", "other"]) 
    
    if CURRENT_OS not in supported_os:
        console.print(f"\n[bold yellow]  WARNING: This tool is officially optimized for {', '.join(supported_os).upper()}[/]")
        console.print(f"[yellow]Your current OS is: [bold red]{CURRENT_OS.upper()}[/][/yellow]")
        
        proceed = Confirm.ask("[bold red]Do you still want to force the installation?[/]")
        if not proceed:
            console.print("[cyan]Installation cancelled by user.[/]")
            return

    if not repo_url:
        console.print(f"[bold red]Error: URL missing for {tool_name}![/]")
        return

    safe_name = tool_name.replace(" ", "_").replace("/", "_")
    install_dir = os.path.join(INSTALL_DEST_DIR, safe_name)

    # 1. Dependency check
    if not check_dependencies(tool_data.get("dependency", [])): 
        return

    # 2. Tool Download / Update (Using Secure Lists)
    if pkg_manager == "git":
        if os.path.exists(install_dir):
            cmd = ["git", "-C", install_dir, "pull"]
            desc = f"Updating {tool_name}..."
        else:
            cmd = ["git", "clone", repo_url, install_dir]
            desc = f"Cloning {tool_name}..."
    elif pkg_manager == "curl":
        if not os.path.exists(install_dir):
            os.makedirs(install_dir)
        filename = repo_url.split("/")[-1]
        cmd = ["curl", "-Lo", os.path.join(install_dir, filename), repo_url]
        desc = f"Downloading {tool_name}..."
    else:
        console.print(f"[red]Error: Unsupported package manager '{pkg_manager}'[/]")
        return

    success, _ = run_command(cmd, desc)
    if not success:
        console.print(f"[bold red]Installation Failed![/] Check logs in {LOG_FILE}")
        return

    # 3. Post Install (Secure permissions setup)
    if CURRENT_OS != "windows":
        run_command(["find", install_dir, "-type", "f", "-name", "*.sh", "-exec", "chmod", "+x", "{}", ";"], "Setting up secure permissions (.sh)...")
        run_command(["find", install_dir, "-type", "f", "-name", "*.py", "-exec", "chmod", "+x", "{}", ";"], "Setting up secure permissions (.py)...")
    
    # 4. Success Message
    msg = Text()
    msg.append(f" {tool_name} Installed Successfully!\n", style="bold green")
    msg.append(f" Folder Path: {install_dir}\n", style="cyan")
    
    console.print(Panel(msg, title="Success", border_style="green"))
    
    # >> Update Installed History
    try:
        with open(INSTALLED_TOOLS_FILE, "a", encoding='utf-8') as f:
            f.write(f"{tool_key}|{install_dir}\n")
    except Exception as e:
        console.print(f"[yellow]Warning: Failed to save history: {e}[/]")
