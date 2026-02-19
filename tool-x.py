# File: tool-x.py
# Author: Lokesh Kumar
# Update: 19/02/2026


import os
import sys
import json
import time
import shutil
import difflib
import math
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.prompt import Prompt, Confirm
from rich import box
from rich.text import Text

# Initialize Console
console = Console()

# --- Import Core Modules ---
try:
    from core.tool_data import TOOLS, TOOL_CATEGORIES
    from core.installation_logic import install_github_tool, LOG_FILE, INSTALLED_TOOLS_FILE
except ImportError as e:
    console.print(f"[bold red]CRITICAL ERROR:[/] Could not import core modules.\nDetails: {e}")
    sys.exit(1)

# File path for Favorites
FAV_FILE = os.path.expanduser("~/tool-x_favs.json")

class ToolX:
    def __init__(self):
        self.version = "2.1 (Multi-Platform)"
        self.favorites = self.load_favorites()

    def load_favorites(self):
        if os.path.exists(FAV_FILE):
            try:
                with open(FAV_FILE, 'r') as f: return json.load(f)
            except: return []
        return []

    def save_favorites(self):
        with open(FAV_FILE, 'w') as f: json.dump(self.favorites, f)

    def toggle_favorite(self, tool_uid):
        if tool_uid in self.favorites:
            self.favorites.remove(tool_uid)
            console.print(f"[yellow]Removed from favorites: {tool_uid}[/]")
        else:
            self.favorites.append(tool_uid)
            console.print(f"[green]Added to favorites: {tool_uid}[/]")
        self.save_favorites()

    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def display_banner(self):
        self.clear_screen()
        title = """
████████╗ ██████╗  ██████╗ ██╗         ██╗  ██╗
╚══██╔══╝██╔═══██╗██╔═══██╗██║         ╚██╗██╔╝
   ██║   ██║   ██║██║   ██║██║          ╚███╔╝ 
   ██║   ██║   ██║██║   ██║██║          ██╔██╗ 
   ██║   ╚██████╔╝╚██████╔╝███████╗    ██╔╝ ██╗
   ╚═╝    ╚═════╝  ╚═════╝ ╚══════╝    ╚═╝  ╚═╝
        """
        info_text = f"[bold cyan]The Apex  Framework[/] | Ver: [green]{self.version}[/]"
        console.print(Panel(f"[bold magenta]{title}[/]\n{info_text}", border_style="bright_blue"))

    def search_tool_menu(self):
        self.display_banner()
        console.print("[bold yellow]---  Smart Search ---[/]")
        query = Prompt.ask("Enter keyword").lower()
        if not query: return

        found_tools = []
        all_names = []
        tool_map = {}

        for cat_id, tools in TOOLS.items():
            for tool_id, data in tools.items():
                name = data['name']
                uid = f"{cat_id}-{tool_id}"
                tool_map[name] = uid
                all_names.append(name)
                if query in name.lower() or query in data['desc'].lower():
                    found_tools.append((uid, name, data['desc']))

        if not found_tools:
            # Fuzzy match
            matches = difflib.get_close_matches(query, all_names, n=3, cutoff=0.4)
            for m in matches:
                uid = tool_map[m]
                cid, tid = uid.split('-')
                found_tools.append((uid, m, TOOLS[cid][tid]['desc']))

        if not found_tools:
            console.print(f"[red]No results for '{query}'[/]")
        else:
            table = Table(box=box.ROUNDED, expand=True)
            table.add_column("UID", style="cyan", no_wrap=True)
            table.add_column("Name", style="green")
            table.add_column("Description", style="white") 
            
            for uid, name, desc in found_tools:
                table.add_row(uid, name, desc)
            console.print(table)
            console.print("[dim]Use these UIDs in Main Menu to install.[/]")
        Prompt.ask("\n[green]Press Enter[/]")

    def uninstall_menu(self):
        self.display_banner()
        if not os.path.exists(INSTALLED_TOOLS_FILE):
            console.print("[yellow]No installed tools found.[/]"); time.sleep(1); return

        with open(INSTALLED_TOOLS_FILE, 'r') as f: lines = [l for l in f.readlines() if l.strip()]
        
        if not lines: console.print("[yellow]No installed tools.[/]"); time.sleep(1); return

        table = Table(box=box.SIMPLE, expand=True)
        table.add_column("#", style="cyan")
        table.add_column("Name", style="white")
        table.add_column("Path", style="dim", overflow="fold") # Responsive path

        installed_map = {}
        for idx, line in enumerate(lines):
            try:
                name, path = line.strip().split('|')
                table.add_row(str(idx+1), name, path)
                installed_map[str(idx+1)] = (name, path, line)
            except: continue

        console.print(table)
        choice = Prompt.ask("[red]Uninstall #[/]", default="00")
        if choice == "00": return

        if choice in installed_map:
            name, path, entry = installed_map[choice]
            if Confirm.ask(f"[bold red]Delete {name}?[/]"):
                if os.path.exists(path):
                    shutil.rmtree(path, ignore_errors=True)
                    console.print(f"[green]Deleted.[/]")
                lines.remove(entry)
                with open(INSTALLED_TOOLS_FILE, 'w') as f: f.writelines(lines)
                time.sleep(1)

    def show_favorites(self):
        self.display_banner()
        console.print("[bold yellow]★ My Favorites[/]")
        if not self.favorites:
            console.print("[dim]No favorites. Use 'fav <id>' in menu.[/]")
        else:
            table = Table(box=box.SIMPLE, expand=True)
            table.add_column("UID", style="cyan")
            table.add_column("Name", style="green")
            for uid in self.favorites:
                try:
                    c, t = uid.split('-')
                    if c in TOOLS and t in TOOLS[c]:
                        table.add_row(uid, TOOLS[c][t]['name'])
                except: continue
            console.print(table)
        Prompt.ask("\n[green]Press Enter[/]")

    def install_flow(self, category_id):
        """Paginated Menu System"""
        PAGE_SIZE = 10
        current_page = 0
        
        # Convert dictionary to list for pagination
        all_tools = []
        tools_dict = TOOLS.get(category_id, {})
        sorted_ids = sorted(tools_dict.keys()) # Keep them in order 01, 02...
        
        for tid in sorted_ids:
            all_tools.append((tid, tools_dict[tid]))

        total_tools = len(all_tools)
        total_pages = math.ceil(total_tools / PAGE_SIZE)

        while True:
            self.display_banner()
            cat_name = TOOL_CATEGORIES.get(category_id, "Unknown")
            console.print(f"[bold blue]Category: {cat_name}[/]", justify="center")
            
            # Pagination Logic
            start_idx = current_page * PAGE_SIZE
            end_idx = start_idx + PAGE_SIZE
            current_batch = all_tools[start_idx:end_idx]

            # Responsive Table
            table = Table(box=box.ROUNDED, show_header=True, header_style="bold magenta", expand=True)
            table.add_column("ID", style="cyan", width=4, no_wrap=True)
            table.add_column("★", style="yellow", width=2)
            table.add_column("Tool Name", style="bold white", width=20)
            table.add_column("Description", style="dim white") # Will wrap automatically

            for tid, data in current_batch:
                uid = f"{category_id}-{tid}"
                fav = "★" if uid in self.favorites else ""
                table.add_row(tid, fav, data['name'], data['desc'])

            console.print(table)
            
            # Navigation & Info Footer
            page_info = f"Page [bold green]{current_page + 1}/{total_pages}[/]"
            nav_help = "[N]ext [P]rev [B]ack"
            console.print(Panel(f"{page_info} | {nav_help}", border_style="dim"))
            
            # Input Prompt
            user_input = Prompt.ask("[bold yellow]Select Tool ID / Command[/]").strip().lower()

            # Navigation Commands
            if user_input == 'b' or user_input == '00': break
            elif user_input == 'n':
                if current_page < total_pages - 1: current_page += 1
                else: console.print("[red]Last Page![/]"); time.sleep(0.5)
            elif user_input == 'p':
                if current_page > 0: current_page -= 1
                else: console.print("[red]First Page![/]"); time.sleep(0.5)
            
            # Tool Action Commands
            else:
                commands = user_input.replace(',', ' ').split()
                skip_next = False
                
                for idx, cmd in enumerate(commands):
                    if skip_next: skip_next = False; continue

                    # Handle Favorites
                    if cmd == "fav":
                        if idx + 1 < len(commands):
                            tid = commands[idx+1].zfill(2)
                            self.toggle_favorite(f"{category_id}-{tid}")
                            skip_next = True
                            time.sleep(0.5)
                        continue

                    # Handle Install
                    tid = cmd.zfill(2)
                    if tid in tools_dict:
                        # Check if tool is on current page (Optional UX, but we allow installing any ID)
                        console.print(f"\n[cyan]>>> Queuing: {tools_dict[tid]['name']}[/]")
                        install_github_tool(tid, category_id)
                    else:
                        console.print(f"[red]Invalid ID: {tid}[/]")
                
                if len(commands) > 0 and commands[0] not in ['n','p']:
                    Prompt.ask("\n[green]Process Completed. Press Enter.[/]")

    def main_menu(self):
        while True:
            self.display_banner()
            menu = Table(show_header=False, box=None, expand=True)
            menu.add_column("ID", style="bold cyan", width=6)
            menu.add_column("Option", style="bold white")

            for cid, cname in TOOL_CATEGORIES.items():
                menu.add_row(f"[{cid}]", cname)

            menu.add_row("", "")
            menu.add_row("[97]", "Search Tool")
            menu.add_row("[98]", "Uninstall Tools")
            menu.add_row("[99]", "Update Tool-X")
            menu.add_row("[F]", "[yellow]★ Favorites[/]")
            menu.add_row("[00]", "[red]Exit[/]")

            console.print(Panel(menu, title="Main Menu", border_style="green"))
            choice = Prompt.ask("[bold yellow]Option[/]")

            if choice == '00': sys.exit()
            elif choice.lower() == 'f': self.show_favorites()
            elif choice == '97': self.search_tool_menu()
            elif choice == '98': self.uninstall_menu()
            elif choice == '99': 
                os.system("git pull"); time.sleep(2); os.execv(sys.executable, ['python'] + sys.argv)
            elif choice in TOOL_CATEGORIES: self.install_flow(choice)
            else: console.print("[red]Invalid![/]"); time.sleep(0.5)

if __name__ == "__main__":
    try:
        app = ToolX()
        app.main_menu()
    except KeyboardInterrupt:
        console.print("\n[red]Exiting...[/]"); sys.exit(0)
