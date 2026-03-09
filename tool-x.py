# File: tool-x.py
# Developer: Lokesh Kumar
# Framework Version: 2.0 
# Update: 08/03/2026
#>> TOOL-X MAIN

import os
import sys
import json
import time
import shutil
import difflib
import math
import platform
import socket
import getpass
from datetime import datetime

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.prompt import Prompt, Confirm
from rich import box
from rich.text import Text
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn

console = Console()

# <> Import Core Modules <>
try:
    from core.tool_data import RAW_TOOLS, TOOLS_BY_CATEGORY, TOOL_CATEGORIES
    from core.installation_logic import install_tool, LOG_FILE, INSTALLED_TOOLS_FILE, TOOLX_SYSTEM_DIR
except ImportError as e:
    console.print(f"[bold red]CRITICAL ERROR:[/] Could not import core modules.\nDetails: {e}")
    sys.exit(1)

# System Files
FAV_FILE = os.path.join(TOOLX_SYSTEM_DIR, "favorites.json")

class ToolX:
    def __init__(self):
        self.version = "2.0 (Master Framework)"
        self.favorites = self.load_favorites()
        self.boot_sequence()

    def get_system_info(self):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
            s.close()
        except:
            ip = "127.0.0.1 (Offline)"

        return {
            "User": getpass.getuser(),
            "OS": platform.system() + " " + platform.release(),
            "Architecture": platform.machine(),
            "Local IP": ip,
            "Date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

    def boot_sequence(self):
        self.clear_screen()
        console.print("\n[bold cyan]SYSTEM INITIALIZATION PROTOCOL STARTED...[/]\n")
        
        with Progress(
            SpinnerColumn(spinner_name="dots2"),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(bar_width=40, style="magenta", complete_style="cyan"),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
        ) as progress:
            
            task1 = progress.add_task("[bold green]Loading Core Modules...", total=100)
            task2 = progress.add_task("[bold yellow]Decrypting Tool Database...", total=100)
            task3 = progress.add_task("[bold red]Establishing Secure Environment...", total=100)

            while not progress.finished:
                progress.update(task1, advance=0.8)
                if progress.tasks[0].percentage > 30:
                    progress.update(task2, advance=0.6)
                if progress.tasks[1].percentage > 50:
                    progress.update(task3, advance=1.0)
                time.sleep(0.04)

        time.sleep(0.5)
        self.clear_screen()
        sys_info = self.get_system_info()
        
        info_text = Text()
        info_text.append(f"[*] Target User      : ", style="bold cyan")
        info_text.append(f"{sys_info['User']}\n", style="bold white")
        info_text.append(f"[*] Operating System : ", style="bold cyan")
        info_text.append(f"{sys_info['OS']}\n", style="bold white")
        info_text.append(f"[*] Architecture     : ", style="bold cyan")
        info_text.append(f"{sys_info['Architecture']}\n", style="bold white")
        info_text.append(f"[*] Local IP Address : ", style="bold cyan")
        info_text.append(f"{sys_info['Local IP']}\n", style="bold white")
        info_text.append(f"[*] Timestamp        : ", style="bold cyan")
        info_text.append(f"{sys_info['Date']}", style="bold white")

        console.print(Panel(info_text, title="[bold red]SYSTEM SCAN COMPLETE[/]", border_style="red", expand=False))
        console.print("\n[bold green]>>> Access Granted. Welcome to Tool-X Master Framework.[/]")
        time.sleep(3.5) 

    def load_favorites(self):
        if os.path.exists(FAV_FILE):
            try:
                with open(FAV_FILE, 'r') as f: return json.load(f)
            except: return []
        return []

    def save_favorites(self):
        try:
            with open(FAV_FILE, 'w') as f: json.dump(self.favorites, f)
        except Exception as e:
            console.print(f"[red]Error saving favorites: {e}[/]")

    def toggle_favorite(self, tool_key):
        if tool_key in self.favorites:
            self.favorites.remove(tool_key)
            console.print(f"[yellow]Removed from favorites: {RAW_TOOLS[tool_key].get('name', tool_key)}[/]")
        else:
            self.favorites.append(tool_key)
            console.print(f"[green]Added to favorites: {RAW_TOOLS[tool_key].get('name', tool_key)}[/]")
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
        info_text = f"[bold cyan]The Apex Master Framework[/] | Version: [green]{self.version}[/]\n[dim]Developer: Lokesh Kumar[/]"
        console.print(Panel(f"[bold magenta]{title}[/]\n{info_text}", border_style="bright_blue"))

    def search_tool_menu(self):
        self.display_banner()
        console.print("[bold yellow]<>  Smart Search <>[/]")
        query = Prompt.ask("Enter tool name or keyword").lower()
        if not query: return

        found_tools = []
        all_names = list(RAW_TOOLS.keys())

        for tool_key, data in RAW_TOOLS.items():
            name = data.get('name', '').lower()
            desc = data.get('desc', '').lower()
            if query in name or query in desc:
                found_tools.append((tool_key, data))

        if not found_tools:
            matches = difflib.get_close_matches(query, all_names, n=5, cutoff=0.4)
            for m in matches:
                found_tools.append((m, RAW_TOOLS[m]))

        if not found_tools:
            console.print(f"[red]No results found for '{query}'. Please try again.[/]")
        else:
            # Map search results to numeric IDs
            tool_mapping = {str(idx + 1): key for idx, (key, _) in enumerate(found_tools)}
            
            table = Table(box=box.ROUNDED, expand=True)
            table.add_column("ID", style="cyan", justify="right", width=5)
            table.add_column("Tool Name", style="green")
            table.add_column("Description", style="white") 
            
            for idx, (key, data) in enumerate(found_tools):
                desc = data.get('desc', 'No description available')
                table.add_row(str(idx + 1), data.get('name', key), desc[:60] + "..." if len(desc)>60 else desc)
            console.print(table)
            
            install_id = Prompt.ask("[bold yellow]Enter Tool ID to install (or press Enter to go back)[/]").strip()
            if install_id in tool_mapping:
                install_tool(tool_mapping[install_id])
            elif install_id:
                console.print("[red]Invalid ID![/]"); time.sleep(1)

        Prompt.ask("\n[green]Press Enter to return to Main Menu[/]")

    def uninstall_menu(self):
        self.display_banner()
        if not os.path.exists(INSTALLED_TOOLS_FILE):
            console.print("[yellow]No installed tools found.[/]"); time.sleep(1.5); return

        try:
            with open(INSTALLED_TOOLS_FILE, 'r') as f: 
                lines = [l for l in f.readlines() if l.strip()]
        except: return
        
        if not lines: console.print("[yellow]You haven't installed any tools yet.[/]"); time.sleep(1.5); return

        table = Table(box=box.SIMPLE, expand=True)
        table.add_column("ID", style="cyan", justify="right", width=5)
        table.add_column("Tool Name", style="white")
        table.add_column("Install Path", style="dim", overflow="fold")

        installed_map = {}
        for idx, line in enumerate(lines):
            try:
                name, path = line.strip().split('|')
                table.add_row(str(idx+1), name, path)
                installed_map[str(idx+1)] = (name, path, line)
            except: continue

        console.print(table)
        choice = Prompt.ask("[red]Select ID to uninstall (00 to go back)[/]").strip()
        # Handle 1 -> 01 or direct numeric matching
        if choice.isdigit() and len(choice) == 1 and choice != '0':
            choice = choice # Uninstall map doesn't use zero-padding
            
        if choice in ['00', '0']: return

        if choice in installed_map:
            name, path, entry = installed_map[choice]
            if Confirm.ask(f"[bold red]Are you sure you want to delete {name}?[/]"):
                if os.path.exists(path):
                    shutil.rmtree(path, ignore_errors=True)
                    console.print(f"[green] Successfully deleted.[/]")
                lines.remove(entry)
                with open(INSTALLED_TOOLS_FILE, 'w') as f: f.writelines(lines)
                time.sleep(1.5)

    def show_favorites(self):
        self.display_banner()
        console.print("[bold yellow]★ My Favorite Tools[/]")
        if not self.favorites:
            console.print("[dim]Your list is empty. Use 'fav <ID>' in menus to add tools.[/]")
        else:
            # Map favorites to numeric IDs
            tool_mapping = {str(idx + 1): key for idx, key in enumerate(self.favorites) if key in RAW_TOOLS}
            
            table = Table(box=box.SIMPLE, expand=True)
            table.add_column("ID", style="cyan", justify="right", width=5)
            table.add_column("Tool Name", style="green")
            
            for num_id, key in tool_mapping.items():
                table.add_row(num_id, RAW_TOOLS[key].get('name', key))
            console.print(table)
            
            install_id = Prompt.ask("\n[bold yellow]Enter Tool ID to install (or press Enter to go back)[/]").strip()
            if install_id in tool_mapping:
                install_tool(tool_mapping[install_id])
            elif install_id:
                console.print("[red]Invalid ID![/]"); time.sleep(1)
        
        Prompt.ask("\n[green]Press Enter to return to Main Menu[/]")

    def show_all_tools(self):
        """NEW FUNCTION: Shows all tools paginated with numeric IDs"""
        all_tools = list(RAW_TOOLS.items())
        total_tools = len(all_tools)
        
        # Create a mapping for numeric IDs (1 to 1000+)
        tool_mapping = {str(idx + 1): key for idx, (key, _) in enumerate(all_tools)}
        
        PAGE_SIZE = 15
        current_page = 0
        total_pages = math.ceil(total_tools / PAGE_SIZE)

        while True:
            self.display_banner()
            console.print(f"[bold blue] All Available Tools ({total_tools} Tools)[/]", justify="center")
            
            start_idx = current_page * PAGE_SIZE
            end_idx = start_idx + PAGE_SIZE
            current_batch = all_tools[start_idx:end_idx]

            table = Table(box=box.ROUNDED, show_header=True, header_style="bold magenta", expand=True)
            table.add_column("ID", style="cyan", justify="right", width=5)
            table.add_column("★", style="yellow", width=3)
            table.add_column("Tool Name", style="bold white", width=25)
            table.add_column("Description", style="dim white")

            for i, (t_key, data) in enumerate(current_batch):
                numeric_id = str(start_idx + i + 1)
                fav = "[yellow]★[/]" if t_key in self.favorites else ""
                desc = data.get('desc', 'No description available')
                table.add_row(numeric_id, fav, data.get('name', t_key), desc[:55] + "..." if len(desc)>55 else desc)

            console.print(table)
            
            page_info = f"Page [bold green]{current_page + 1}/{total_pages}[/]"
            nav_help = "[N] Next | [P] Prev | [B] Back"
            console.print(Panel(f"{page_info} | {nav_help}", border_style="dim"))
            
            user_input = Prompt.ask("[bold yellow]Enter Tool ID to install (or Command)[/]").strip()

            if user_input.lower() in ['b', '00', 'back']: break
            elif user_input.lower() == 'n':
                if current_page < total_pages - 1: current_page += 1
                else: console.print("[red]Already on the last page![/]"); time.sleep(0.5)
            elif user_input.lower() == 'p':
                if current_page > 0: current_page -= 1
                else: console.print("[red]Already on the first page![/]"); time.sleep(0.5)
            else:
                # Handle install or favorite
                parts = user_input.lower().split()
                if len(parts) == 2 and parts[0] == "fav":
                    fav_id = parts[1]
                    if fav_id in tool_mapping:
                        self.toggle_favorite(tool_mapping[fav_id])
                    else:
                        console.print("[red]Invalid Tool ID for favorite![/]")
                    time.sleep(0.8)
                elif user_input in tool_mapping:
                    real_key = tool_mapping[user_input]
                    console.print(f"\n[cyan]>>> Preparing to install: {RAW_TOOLS[real_key].get('name', real_key)}[/]")
                    install_tool(real_key)
                    Prompt.ask("\n[green]Process completed. Press Enter to go back.[/]")
                else:
                    console.print(f"[red]Invalid Tool ID or Command: {user_input}[/]"); time.sleep(1)

    def install_flow(self, cat_id):
        cat_name = TOOL_CATEGORIES.get(cat_id)
        if not cat_name: return
        
        tools_in_cat = TOOLS_BY_CATEGORY.get(cat_name, {})
        all_tools = list(tools_in_cat.items())
        
        PAGE_SIZE = 15
        current_page = 0
        total_tools = len(all_tools)
        if total_tools == 0:
            console.print("[red]No tools found in this category.[/]"); time.sleep(1); return
            
        total_pages = math.ceil(total_tools / PAGE_SIZE)

        # Mapping sequential IDs just for this specific category list
        tool_mapping = {str(idx + 1): key for idx, (key, _) in enumerate(all_tools)}

        while True:
            self.display_banner()
            display_cat_name = cat_name.replace('_', ' ').title()
            console.print(f"[bold blue]Category: {display_cat_name} ({total_tools} Tools)[/]", justify="center")
            
            start_idx = current_page * PAGE_SIZE
            end_idx = start_idx + PAGE_SIZE
            current_batch = all_tools[start_idx:end_idx]

            table = Table(box=box.ROUNDED, show_header=True, header_style="bold magenta", expand=True)
            table.add_column("ID", style="cyan", justify="right", width=5)
            table.add_column("★", style="yellow", width=3)
            table.add_column("Tool Name", style="bold white", width=25)
            table.add_column("Description", style="dim white")

            for i, (t_key, data) in enumerate(current_batch):
                numeric_id = str(start_idx + i + 1)
                fav = "[yellow]★[/]" if t_key in self.favorites else ""
                desc = data.get('desc', 'No description available')
                table.add_row(numeric_id, fav, data.get('name', t_key), desc[:55] + "..." if len(desc)>55 else desc)

            console.print(table)
            
            page_info = f"Page [bold green]{current_page + 1}/{total_pages}[/]"
            nav_help = "[N] Next | [P] Prev | [B] Back"
            console.print(Panel(f"{page_info} | {nav_help}", border_style="dim"))
            
            user_input = Prompt.ask("[bold yellow]Enter Tool ID to install (or Command)[/]").strip()

            if user_input.lower() in ['b', '00', 'back']: break
            elif user_input.lower() == 'n':
                if current_page < total_pages - 1: current_page += 1
                else: console.print("[red]Already on the last page![/]"); time.sleep(0.5)
            elif user_input.lower() == 'p':
                if current_page > 0: current_page -= 1
                else: console.print("[red]Already on the first page![/]"); time.sleep(0.5)
            else:
                parts = user_input.lower().split()
                if len(parts) == 2 and parts[0] == "fav":
                    fav_id = parts[1]
                    if fav_id in tool_mapping:
                        self.toggle_favorite(tool_mapping[fav_id])
                    else:
                        console.print("[red]Invalid Tool ID for favorite![/]")
                    time.sleep(0.8)
                elif user_input in tool_mapping:
                    real_key = tool_mapping[user_input]
                    console.print(f"\n[cyan]>>> Preparing to install: {RAW_TOOLS[real_key].get('name', real_key)}[/]")
                    install_tool(real_key)
                    Prompt.ask("\n[green]Process completed. Press Enter to go back.[/]")
                else:
                    console.print(f"[red]Invalid Tool ID or Command: {user_input}[/]"); time.sleep(1)

    def main_menu(self):
        while True:
            self.display_banner()
            
            # <> 2-Column Layout for Categories <>
            menu = Table(show_header=False, box=None, expand=True)
            menu.add_column("ID1", style="bold cyan", justify="right", width=6)
            menu.add_column("Opt1", style="bold white")
            menu.add_column("ID2", style="bold cyan", justify="right", width=6)
            menu.add_column("Opt2", style="bold white")

            cat_items = list(TOOL_CATEGORIES.items())
            half = math.ceil(len(cat_items) / 2)
            
            for i in range(half):
                id1, name1 = cat_items[i]
                name1_clean = name1.replace("_", " ").title()
                
                if i + half < len(cat_items):
                    id2, name2 = cat_items[i + half]
                    name2_clean = name2.replace("_", " ").title()
                    menu.add_row(f"[{id1}]", name1_clean, f"[{id2}]", name2_clean)
                else:
                    menu.add_row(f"[{id1}]", name1_clean, "", "")

            # <> Bottom Menu for Utilities <>
            utils_table = Table(show_header=False, box=None, expand=True)
            utils_table.add_column("ID", style="bold cyan", justify="right", width=6)
            utils_table.add_column("Option", style="bold white")
            
            utils_table.add_row("[96]", " Show All Tools")  
            utils_table.add_row("[97]", " Smart Search")
            utils_table.add_row("[98]", " Uninstall Tools")
            utils_table.add_row("[99]", " Update Tool-X")
            utils_table.add_row("[F]", "[yellow]★ My Favorites[/]")
            utils_table.add_row("[00]", "[red]Exit[/]")

            console.print(Panel(menu, title="[bold green]Available Categories[/]", border_style="green"))
            console.print(Panel(utils_table, title="[bold blue]Utilities & Settings[/]", border_style="blue"))
            
            choice = Prompt.ask("[bold yellow]Select Option[/]").strip()

            if choice.isdigit() and len(choice) == 1 and choice != '0':
                choice = choice.zfill(2)
            elif choice == '0':
                choice = '00'

            if choice == '00': 
                console.print("[green]Goodbye! Thank you for using Tool-X.[/]")
                sys.exit()
            elif choice.lower() == 'f': self.show_favorites()
            elif choice == '96': self.show_all_tools()
            elif choice == '97': self.search_tool_menu()
            elif choice == '98': self.uninstall_menu()
            elif choice == '99': 
                console.print("[cyan]Checking for updates...[/]")
                os.system("git pull"); time.sleep(2); os.execv(sys.executable, ['python'] + sys.argv)
            elif choice in TOOL_CATEGORIES: self.install_flow(choice)
            else: console.print("[red]Invalid Option![/]"); time.sleep(0.5)

if __name__ == "__main__":
    try:
        app = ToolX()
        app.main_menu()
    except KeyboardInterrupt:
        console.print("\n[red]Exiting...[/]"); sys.exit(0)
