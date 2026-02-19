# File: core/installation_logic.py
# Update: 19/02/2026
import os
import time
import subprocess
import shutil
import platform
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.panel import Panel
from rich.text import Text

# Import tool definitions
from core.tool_data import TOOLS

HOME_DIR = os.path.expanduser("~")
LOG_FILE = os.path.join(HOME_DIR, "tool-x_error.log")
INSTALLED_TOOLS_FILE = os.path.join(HOME_DIR, "tool-x_installed.json")

console = Console()

def run_command(command, description, cwd=None):
    """Runs shell commands with a loading spinner."""
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True,
    ) as progress:
        progress.add_task(description=description, total=None)
        try:
            result = subprocess.run(
                command, shell=True, cwd=cwd, capture_output=True, text=True
            )
            if result.returncode != 0:
                timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
                with open(LOG_FILE, "a", encoding='utf-8') as f:
                    f.write(f"\n[{timestamp}] FAILED: {command}\nERROR: {result.stderr}\n")
                return False, result.stderr
            return True, result.stdout
        except Exception as e:
            return False, str(e)

def check_dependencies(reqs):
    """Installs required packages automatically (Smart Check)."""
    if not reqs: return True
    
    # Clean up requirements string
    req_list = reqs.replace(',', ' ').split()
    
    for pkg in req_list:
        pkg = pkg.strip()
        if not pkg: continue
        
        # 'bash' is built-in mostly, skip to save time
        if pkg == "bash": continue

        # Check if already installed
        if shutil.which(pkg): continue
        
        console.print(f"[dim]Installing dependency: {pkg}...[/]")
        
        # Installation command based on OS
        if platform.system() == "Windows":
             console.print(f"[yellow]Skipping auto-install for '{pkg}' on Windows (Install manually).[/]")
             continue
        else:
             install_cmd = f"pkg install -y {pkg}"
        
        success, _ = run_command(install_cmd, f"Installing {pkg}...")
        if not success:
            console.print(f"[bold red]Failed to install dependency: {pkg}[/]")
            return False
    return True

def install_github_tool(tool_id, category_id):
    """Main installation logic."""
    try:
        tool_data = TOOLS[category_id][tool_id]
    except KeyError:
        console.print("[bold red]Error: Tool ID not found.[/]")
        return

    tool_name = tool_data["name"]
    repo_url = tool_data["repo"]
    safe_name = tool_name.replace(" ", "_").replace("/", "_")
    install_dir = os.path.join(HOME_DIR, safe_name)

    # 1. Check Dependencies
    if not check_dependencies(tool_data.get("reqs", "")): return

    # 2. Clone/Update
    if os.path.exists(install_dir):
        cmd, desc = f"git -C {install_dir} pull", f"Updating {tool_name}..."
    else:
        cmd, desc = f"git clone {repo_url} {install_dir}", f"Cloning {tool_name}..."

    success, _ = run_command(cmd, desc)
    if not success:
        console.print(f"[bold red]Installation Failed![/] Check {LOG_FILE}")
        return

    # 3. Post Install (Permissions)
    run_command(f"chmod -R 777 {install_dir}", "Fixing permissions...")
    
    # 4. Success Message
    # If help_cmd is just 'ls', we give a generic helpful message
    help_cmd = tool_data.get('help_cmd', 'ls')
    if help_cmd == "ls":
        run_msg = f"cd {safe_name} && ls"
        hint = "(Check README.md inside the folder)"
    else:
        run_msg = f"cd {safe_name} && {help_cmd}"
        hint = ""

    msg = Text()
    msg.append(f"✅ {tool_name} Installed Successfully!\n", style="bold green")
    msg.append(f"📂 Location: {install_dir}\n", style="cyan")
    msg.append(f"🚀 To Start:\n", style="yellow")
    msg.append(f"   {run_msg}\n", style="bold white")
    if hint:
        msg.append(f"   {hint}", style="dim")
    
    console.print(Panel(msg, title="Success", border_style="green"))
    
    # Update Installed History
    try:
        with open(INSTALLED_TOOLS_FILE, "a", encoding='utf-8') as f:
            f.write(f"{tool_name}|{install_dir}\n")
    except:
        pass 
