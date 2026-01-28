#!/usr/bin/env python3
"""
╔═══════════════════════════════════════════════════════════════════════════╗
║                      Snipe-IT Lazy Cli                                    ║
║                      Asset Management Tool                                ║
╚═══════════════════════════════════════════════════════════════════════════╝
Lazy to open the Web UI? Use this CLI to manage a basic operation of your Snipe-IT assets
"""

import requests
import json
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from enum import Enum
import sys
import time
from datetime import datetime



SNIPEIT_API_URL = "http://snipe-it-domain/api/v1"
SNIPEIT_API_TOKEN = "API_KEY"



class Colors:
    RESET = '\033[0m'
    BOLD = '\033[1m'
    DIM = '\033[2m'
    UNDERLINE = '\033[4m'
    
    # Foreground colors
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    
    # Bright foreground colors
    BRIGHT_BLACK = '\033[90m'
    BRIGHT_RED = '\033[91m'
    BRIGHT_GREEN = '\033[92m'
    BRIGHT_YELLOW = '\033[93m'
    BRIGHT_BLUE = '\033[94m'
    BRIGHT_MAGENTA = '\033[95m'
    BRIGHT_CYAN = '\033[96m'
    BRIGHT_WHITE = '\033[97m'
    
    # Background colors
    BG_BLACK = '\033[40m'
    BG_RED = '\033[41m'
    BG_GREEN = '\033[42m'
    BG_YELLOW = '\033[43m'
    BG_BLUE = '\033[44m'
    BG_MAGENTA = '\033[45m'
    BG_CYAN = '\033[46m'
    BG_WHITE = '\033[47m'



class UI:
    
    @staticmethod
    def clear_screen():
        print("\033[2J\033[H", end='')
    
    @staticmethod
    def print_header():
        UI.clear_screen()
        print(f"{Colors.BRIGHT_CYAN}{Colors.BOLD}")
        print("╔═══════════════════════════════════════════════════════════════════════════╗")
        print("║                                                                           ║")
        print("║                    🎯 SNIPE-IT Lazy Cli 🎯                               ║")
        print("║                                                                           ║")
        print("║                      Asset Management Tool                                ║")
        print("║                                                                           ║")
        print("╚═══════════════════════════════════════════════════════════════════════════╝")
        print(f"{Colors.RESET}\n")
    
    @staticmethod
    def print_menu():
        print(f"{Colors.BRIGHT_YELLOW}{Colors.BOLD}╭─────────────────────────────────────────────╮{Colors.RESET}")
        print(f"{Colors.BRIGHT_YELLOW}│{Colors.RESET}            {Colors.BOLD}MAIN MENU{Colors.RESET}                      {Colors.BRIGHT_YELLOW}│{Colors.RESET}")
        print(f"{Colors.BRIGHT_YELLOW}╰─────────────────────────────────────────────╯{Colors.RESET}\n")
        
        menu_items = [
            ("1", "📦 List Assets", Colors.BRIGHT_GREEN),
            ("2", "🔑 List Licenses", Colors.BRIGHT_BLUE),
            ("3", "👥 List Users", Colors.BRIGHT_MAGENTA),
            ("4", "🏷️  List Categories", Colors.BRIGHT_CYAN),
            ("5", "🏢 List Locations", Colors.BRIGHT_YELLOW),
            ("6", "🔧 List Models", Colors.BRIGHT_WHITE),
            ("", "───────────────────────────────", Colors.DIM),
            ("7", "❌ Delete Asset", Colors.BRIGHT_RED),
            ("8", "❌ Delete License", Colors.BRIGHT_RED),
            ("9", "❌ Delete User", Colors.BRIGHT_RED),
            ("", "───────────────────────────────", Colors.DIM),
            ("10", "📊 Show Statistics", Colors.BRIGHT_CYAN),
            ("11", "🔍 Search Everything", Colors.BRIGHT_MAGENTA),
            ("12", "📡 Real-Time Monitor", Colors.BRIGHT_GREEN),
            ("", "───────────────────────────────", Colors.DIM),
            ("0", "🚪 Exit", Colors.BRIGHT_RED),
        ]
        
        for num, text, color in menu_items:
            if num:
                print(f"  {color}{num:>2}{Colors.RESET}. {text}")
            else:
                print(f"  {color}{text}{Colors.RESET}")
        
        print()
    
    @staticmethod
    def print_box(title: str, content: List[str], color=Colors.BRIGHT_CYAN):

        width = max(len(line) for line in content + [title]) + 4
        width = max(width, 60)
        
        print(f"\n{color}╭{'─' * (width - 2)}╮{Colors.RESET}")
        print(f"{color}│{Colors.RESET} {Colors.BOLD}{title.center(width - 4)}{Colors.RESET} {color}│{Colors.RESET}")
        print(f"{color}╰{'─' * (width - 2)}╯{Colors.RESET}\n")
        
        for line in content:
            print(f"  {line}")
        print()
    
    @staticmethod
    def print_table(headers: List[str], rows: List[List[str]], title: str = ""):

        if not rows:
            UI.print_box("No Data", ["No items found."], Colors.YELLOW)
            return
        
        col_widths = [len(h) for h in headers]
        for row in rows:
            for i, cell in enumerate(row):
                col_widths[i] = max(col_widths[i], len(str(cell)))
        
        if title:
            total_width = sum(col_widths) + len(headers) * 3 + 1
            print(f"\n{Colors.BRIGHT_CYAN}{'═' * total_width}{Colors.RESET}")
            print(f"{Colors.BOLD}{title.center(total_width)}{Colors.RESET}")
            print(f"{Colors.BRIGHT_CYAN}{'═' * total_width}{Colors.RESET}\n")
        

        header_line = "┃ "
        for i, header in enumerate(headers):
            header_line += f"{Colors.BOLD}{Colors.BRIGHT_YELLOW}{header.ljust(col_widths[i])}{Colors.RESET} ┃ "
        print(f"{Colors.BRIGHT_CYAN}┏{'━' * (len(header_line) - len(Colors.BOLD) - len(Colors.BRIGHT_YELLOW) - len(Colors.RESET) * 2 - 4)}┓{Colors.RESET}")
        print(header_line[:-3] + f"{Colors.BRIGHT_CYAN}┃{Colors.RESET}")
        print(f"{Colors.BRIGHT_CYAN}┣{'━' * (len(header_line) - len(Colors.BOLD) - len(Colors.BRIGHT_YELLOW) - len(Colors.RESET) * 2 - 4)}┫{Colors.RESET}")

        for row in rows:
            row_line = "┃ "
            for i, cell in enumerate(row):
                row_line += f"{str(cell).ljust(col_widths[i])} ┃ "
            print(row_line[:-3] + f"{Colors.BRIGHT_CYAN}┃{Colors.RESET}")
        
        print(f"{Colors.BRIGHT_CYAN}┗{'━' * (len(header_line) - len(Colors.BOLD) - len(Colors.BRIGHT_YELLOW) - len(Colors.RESET) * 2 - 4)}┛{Colors.RESET}\n")
    
    @staticmethod
    def print_success(message: str):
        print(f"{Colors.BRIGHT_GREEN}✓ {message}{Colors.RESET}")
    
    @staticmethod
    def print_error(message: str):
        print(f"{Colors.BRIGHT_RED}✗ {message}{Colors.RESET}")
    
    @staticmethod
    def print_info(message: str):
        print(f"{Colors.BRIGHT_BLUE}ℹ {message}{Colors.RESET}")
    
    @staticmethod
    def print_warning(message: str):
        print(f"{Colors.BRIGHT_YELLOW}⚠ {message}{Colors.RESET}")
    
    @staticmethod
    def get_input(prompt: str, color=Colors.BRIGHT_CYAN) -> str:
        return input(f"{color}➤ {prompt}{Colors.RESET} ")
    
    @staticmethod
    def confirm(message: str) -> bool:
        response = UI.get_input(f"{message} (yes/no): ", Colors.BRIGHT_YELLOW).lower()
        return response in ['yes', 'y']
    
    @staticmethod
    def pause():
        UI.get_input(f"{Colors.DIM}Press Enter to continue...{Colors.RESET}", Colors.BRIGHT_BLACK)



class SnipeITClient:
    def __init__(self, api_url: str, api_token: str):
        self.api_url = api_url.rstrip('/')
        self.api_token = api_token
        self.headers = {
            'Authorization': f'Bearer {api_token}',
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }
    
    def _make_request(self, method: str, endpoint: str, **kwargs) -> Optional[Dict]:

        url = f"{self.api_url}/{endpoint.lstrip('/')}"
        
        try:
            response = requests.request(method, url, headers=self.headers, **kwargs)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            UI.print_error(f"API Error: {str(e)}")
            if hasattr(e.response, 'text'):
                UI.print_error(f"Details: {e.response.text}")
            return None
    

    
    def list_assets(self, limit: int = 50, silent: bool = False) -> Optional[List[Dict]]:
        if not silent:
            UI.print_info(f"Fetching assets...")
        data = self._make_request('GET', f'/hardware?limit={limit}')
        return data.get('rows', []) if data else []
    
    def get_asset(self, asset_id: int) -> Optional[Dict]:
        return self._make_request('GET', f'/hardware/{asset_id}')
    
    def delete_asset(self, asset_id: int) -> bool:
        result = self._make_request('DELETE', f'/hardware/{asset_id}')
        return result is not None
    

    def list_licenses(self, limit: int = 50, silent: bool = False) -> Optional[List[Dict]]:
        if not silent:
            UI.print_info(f"Fetching licenses...")
        data = self._make_request('GET', f'/licenses?limit={limit}')
        return data.get('rows', []) if data else []
    
    def get_license(self, license_id: int) -> Optional[Dict]:
        return self._make_request('GET', f'/licenses/{license_id}')
    
    def delete_license(self, license_id: int) -> bool:
        result = self._make_request('DELETE', f'/licenses/{license_id}')
        return result is not None
    

    
    def list_users(self, limit: int = 50, silent: bool = False) -> Optional[List[Dict]]:
        if not silent:
            UI.print_info(f"Fetching users...")
        data = self._make_request('GET', f'/users?limit={limit}')
        return data.get('rows', []) if data else []
    
    def get_user(self, user_id: int) -> Optional[Dict]:
        return self._make_request('GET', f'/users/{user_id}')
    
    def delete_user(self, user_id: int) -> bool:
        result = self._make_request('DELETE', f'/users/{user_id}')
        return result is not None
    

    
    def list_categories(self, limit: int = 50) -> Optional[List[Dict]]:
        UI.print_info(f"Fetching categories...")
        data = self._make_request('GET', f'/categories?limit={limit}')
        return data.get('rows', []) if data else []
    

    def list_locations(self, limit: int = 50) -> Optional[List[Dict]]:
        UI.print_info(f"Fetching locations...")
        data = self._make_request('GET', f'/locations?limit={limit}')
        return data.get('rows', []) if data else []

    def list_models(self, limit: int = 50) -> Optional[List[Dict]]:
        UI.print_info(f"Fetching models...")
        data = self._make_request('GET', f'/models?limit={limit}')
        return data.get('rows', []) if data else []
    

    def get_statistics(self) -> Dict[str, int]:
        stats = {}
        

        endpoints = {
            'Assets': '/hardware',
            'Licenses': '/licenses',
            'Users': '/users',
            'Categories': '/categories',
            'Locations': '/locations',
            'Models': '/models',
        }
        
        for name, endpoint in endpoints.items():
            data = self._make_request('GET', f'{endpoint}?limit=1')
            stats[name] = data.get('total', 0) if data else 0
        
        return stats



class SnipeITManager:
    
    def __init__(self):
        self.client = SnipeITClient(SNIPEIT_API_URL, SNIPEIT_API_TOKEN)
    
    def run(self):
        while True:
            UI.print_header()
            UI.print_menu()
            
            choice = UI.get_input("Select an option")
            
            if choice == '1':
                self.show_assets()
            elif choice == '2':
                self.show_licenses()
            elif choice == '3':
                self.show_users()
            elif choice == '4':
                self.show_categories()
            elif choice == '5':
                self.show_locations()
            elif choice == '6':
                self.show_models()
            elif choice == '7':
                self.delete_asset()
            elif choice == '8':
                self.delete_license()
            elif choice == '9':
                self.delete_user()
            elif choice == '10':
                self.show_statistics()
            elif choice == '11':
                self.search_everything()
            elif choice == '12':
                self.realtime_monitor()
            elif choice == '0':
                self.exit_application()
            else:
                UI.print_error("Invalid option! Please try again.")
                UI.pause()
    
    def show_assets(self):
        UI.clear_screen()
        UI.print_header()
        assets = self.client.list_assets(limit=100)
        
        if not assets:
            UI.print_warning("No assets found or failed to fetch.")
            UI.pause()
            return
        
        headers = ["ID", "Asset Tag", "Name", "Model", "Status", "Location"]
        rows = []
        
        for asset in assets:
            rows.append([
                asset.get('id', 'N/A'),
                asset.get('asset_tag', 'N/A'),
                asset.get('name', 'N/A'),
                asset.get('model', {}).get('name', 'N/A') if asset.get('model') else 'N/A',
                asset.get('status_label', {}).get('name', 'N/A') if asset.get('status_label') else 'N/A',
                asset.get('location', {}).get('name', 'N/A') if asset.get('location') else 'N/A',
            ])
        
        UI.print_table(headers, rows, f"📦 ASSETS (Total: {len(assets)})")
        UI.print_success(f"Displayed {len(assets)} assets")
        UI.pause()
    
    def show_licenses(self):
        UI.clear_screen()
        UI.print_header()
        licenses = self.client.list_licenses(limit=100)
        
        if not licenses:
            UI.print_warning("No licenses found or failed to fetch.")
            UI.pause()
            return
        
        headers = ["ID", "Name", "Product Key", "Seats", "Available", "Category"]
        rows = []
        
        for lic in licenses:
            rows.append([
                lic.get('id', 'N/A'),
                lic.get('name', 'N/A'),
                lic.get('product_key', 'N/A')[:20] + '...' if lic.get('product_key') and len(lic.get('product_key', '')) > 20 else lic.get('product_key', 'N/A'),
                lic.get('seats', 0),
                lic.get('free_seats_count', 0),
                lic.get('category', {}).get('name', 'N/A') if lic.get('category') else 'N/A',
            ])
        
        UI.print_table(headers, rows, f"🔑 LICENSES (Total: {len(licenses)})")
        UI.print_success(f"Displayed {len(licenses)} licenses")
        UI.pause()
    
    def show_users(self):

        UI.clear_screen()
        UI.print_header()
        users = self.client.list_users(limit=100)
        
        if not users:
            UI.print_warning("No users found or failed to fetch.")
            UI.pause()
            return
        
        headers = ["ID", "Username", "First Name", "Last Name", "Email", "Assets"]
        rows = []
        
        for user in users:
            rows.append([
                user.get('id', 'N/A'),
                user.get('username', 'N/A'),
                user.get('first_name', 'N/A'),
                user.get('last_name', 'N/A'),
                user.get('email', 'N/A'),
                user.get('assets_count', 0),
            ])
        
        UI.print_table(headers, rows, f"👥 USERS (Total: {len(users)})")
        UI.print_success(f"Displayed {len(users)} users")
        UI.pause()
    
    def show_categories(self):

        UI.clear_screen()
        UI.print_header()
        categories = self.client.list_categories(limit=100)
        
        if not categories:
            UI.print_warning("No categories found or failed to fetch.")
            UI.pause()
            return
        
        headers = ["ID", "Name", "Type", "Assets Count"]
        rows = []
        
        for cat in categories:
            rows.append([
                cat.get('id', 'N/A'),
                cat.get('name', 'N/A'),
                cat.get('category_type', 'N/A'),
                cat.get('assets_count', 0),
            ])
        
        UI.print_table(headers, rows, f"🏷️  CATEGORIES (Total: {len(categories)})")
        UI.print_success(f"Displayed {len(categories)} categories")
        UI.pause()
    
    def show_locations(self):

        UI.clear_screen()
        UI.print_header()
        locations = self.client.list_locations(limit=100)
        
        if not locations:
            UI.print_warning("No locations found or failed to fetch.")
            UI.pause()
            return
        
        headers = ["ID", "Name", "Address", "City", "Country", "Assets"]
        rows = []
        
        for loc in locations:
            rows.append([
                loc.get('id', 'N/A'),
                loc.get('name', 'N/A'),
                loc.get('address', 'N/A'),
                loc.get('city', 'N/A'),
                loc.get('country', 'N/A'),
                loc.get('assets_count', 0),
            ])
        
        UI.print_table(headers, rows, f"🏢 LOCATIONS (Total: {len(locations)})")
        UI.print_success(f"Displayed {len(locations)} locations")
        UI.pause()
    
    def show_models(self):

        UI.clear_screen()
        UI.print_header()
        models = self.client.list_models(limit=100)
        
        if not models:
            UI.print_warning("No models found or failed to fetch.")
            UI.pause()
            return
        
        headers = ["ID", "Name", "Model Number", "Manufacturer", "Category", "Assets"]
        rows = []
        
        for model in models:
            rows.append([
                model.get('id', 'N/A'),
                model.get('name', 'N/A'),
                model.get('model_number', 'N/A'),
                model.get('manufacturer', {}).get('name', 'N/A') if model.get('manufacturer') else 'N/A',
                model.get('category', {}).get('name', 'N/A') if model.get('category') else 'N/A',
                model.get('assets_count', 0),
            ])
        
        UI.print_table(headers, rows, f"🔧 MODELS (Total: {len(models)})")
        UI.print_success(f"Displayed {len(models)} models")
        UI.pause()
    
    def delete_asset(self):

        UI.clear_screen()
        UI.print_header()
        UI.print_box("Delete Asset", ["Enter the Asset ID to delete"], Colors.BRIGHT_RED)
        
        asset_id = UI.get_input("Asset ID")
        
        if not asset_id.isdigit():
            UI.print_error("Invalid Asset ID!")
            UI.pause()
            return
        
        asset_id = int(asset_id)
        asset = self.client.get_asset(asset_id)
        if not asset:
            UI.print_error(f"Asset with ID {asset_id} not found!")
            UI.pause()
            return
        
        print(f"\n{Colors.BRIGHT_YELLOW}Asset Details:{Colors.RESET}")
        print(f"  ID: {asset.get('id')}")
        print(f"  Tag: {asset.get('asset_tag')}")
        print(f"  Name: {asset.get('name')}")
        print(f"  Model: {asset.get('model', {}).get('name', 'N/A')}")
        print()
        
        if UI.confirm(f"{Colors.BRIGHT_RED}Are you sure you want to delete this asset?{Colors.RESET}"):
            if self.client.delete_asset(asset_id):
                UI.print_success(f"Asset {asset_id} deleted successfully!")
            else:
                UI.print_error(f"Failed to delete asset {asset_id}")
        else:
            UI.print_info("Deletion cancelled.")
        
        UI.pause()
    
    def delete_license(self):
        UI.clear_screen()
        UI.print_header()
        UI.print_box("Delete License", ["Enter the License ID to delete"], Colors.BRIGHT_RED)
        
        license_id = UI.get_input("License ID")
        
        if not license_id.isdigit():
            UI.print_error("Invalid License ID!")
            UI.pause()
            return
        
        license_id = int(license_id)
        license_data = self.client.get_license(license_id)
        if not license_data:
            UI.print_error(f"License with ID {license_id} not found!")
            UI.pause()
            return
        
        print(f"\n{Colors.BRIGHT_YELLOW}License Details:{Colors.RESET}")
        print(f"  ID: {license_data.get('id')}")
        print(f"  Name: {license_data.get('name')}")
        print(f"  Seats: {license_data.get('seats')}")
        print(f"  Available: {license_data.get('free_seats_count')}")
        print()
        
        if UI.confirm(f"{Colors.BRIGHT_RED}Are you sure you want to delete this license?{Colors.RESET}"):
            if self.client.delete_license(license_id):
                UI.print_success(f"License {license_id} deleted successfully!")
            else:
                UI.print_error(f"Failed to delete license {license_id}")
        else:
            UI.print_info("Deletion cancelled.")
        
        UI.pause()
    
    def delete_user(self):
        UI.clear_screen()
        UI.print_header()
        UI.print_box("Delete User", ["Enter the User ID to delete"], Colors.BRIGHT_RED)
        
        user_id = UI.get_input("User ID")
        
        if not user_id.isdigit():
            UI.print_error("Invalid User ID!")
            UI.pause()
            return
        
        user_id = int(user_id)
        user = self.client.get_user(user_id)
        if not user:
            UI.print_error(f"User with ID {user_id} not found!")
            UI.pause()
            return
        
        print(f"\n{Colors.BRIGHT_YELLOW}User Details:{Colors.RESET}")
        print(f"  ID: {user.get('id')}")
        print(f"  Username: {user.get('username')}")
        print(f"  Name: {user.get('first_name')} {user.get('last_name')}")
        print(f"  Email: {user.get('email')}")
        print()
        
        if UI.confirm(f"{Colors.BRIGHT_RED}Are you sure you want to delete this user?{Colors.RESET}"):
            if self.client.delete_user(user_id):
                UI.print_success(f"User {user_id} deleted successfully!")
            else:
                UI.print_error(f"Failed to delete user {user_id}")
        else:
            UI.print_info("Deletion cancelled.")
        
        UI.pause()
    
    def show_statistics(self):
        UI.clear_screen()
        UI.print_header()
        UI.print_info("Fetching comprehensive statistics...")
        
        stats = self.client.get_statistics()
        
        assets = self.client.list_assets(limit=500)
        licenses = self.client.list_licenses(limit=500)
        users = self.client.list_users(limit=500)
        
        total_assets = stats.get('Assets', 0)
        deployed_assets = sum(1 for a in (assets or []) if a.get('status_label', {}).get('status_meta') == 'deployed')
        available_assets = sum(1 for a in (assets or []) if a.get('status_label', {}).get('status_meta') == 'deployable')
        
        total_license_seats = sum(l.get('seats', 0) for l in (licenses or []))
        used_license_seats = sum(l.get('seats', 0) - l.get('free_seats_count', 0) for l in (licenses or []))
        
        active_users = sum(1 for u in (users or []) if u.get('activated'))
        users_with_assets = sum(1 for u in (users or []) if u.get('assets_count', 0) > 0)
        
        print(f"\n{Colors.BRIGHT_CYAN}{'═' * 80}{Colors.RESET}")
        print(f"{Colors.BRIGHT_CYAN}║{Colors.RESET} {Colors.BOLD}{Colors.BRIGHT_WHITE}{'📊 SNIPE-IT ADVANCED STATISTICS DASHBOARD 📊'.center(76)}{Colors.RESET} {Colors.BRIGHT_CYAN}║{Colors.RESET}")
        print(f"{Colors.BRIGHT_CYAN}{'═' * 80}{Colors.RESET}\n")
        
        print(f"{Colors.BRIGHT_GREEN}┌{'─' * 78}┐{Colors.RESET}")
        print(f"{Colors.BRIGHT_GREEN}│{Colors.RESET} {Colors.BOLD}📦 ASSETS OVERVIEW{Colors.RESET}{' ' * 58} {Colors.BRIGHT_GREEN}│{Colors.RESET}")
        print(f"{Colors.BRIGHT_GREEN}└{'─' * 78}┘{Colors.RESET}\n")
        
        print(f"  {Colors.BRIGHT_WHITE}Total Assets:{Colors.RESET} {Colors.BOLD}{Colors.BRIGHT_CYAN}{total_assets}{Colors.RESET}")
        
        if assets:
            deployed_pct = (deployed_assets / total_assets * 100) if total_assets > 0 else 0
            available_pct = (available_assets / total_assets * 100) if total_assets > 0 else 0
            
            print(f"\n  {Colors.BRIGHT_YELLOW}├─ Deployed:{Colors.RESET} {deployed_assets} {Colors.DIM}({deployed_pct:.1f}%){Colors.RESET}")
            self._print_progress_bar(deployed_pct, 50, Colors.BRIGHT_GREEN)
            
            print(f"\n  {Colors.BRIGHT_BLUE}├─ Available:{Colors.RESET} {available_assets} {Colors.DIM}({available_pct:.1f}%){Colors.RESET}")
            self._print_progress_bar(available_pct, 50, Colors.BRIGHT_BLUE)
            
            print(f"\n  {Colors.BRIGHT_MAGENTA}└─ Other Status:{Colors.RESET} {total_assets - deployed_assets - available_assets}")
        
        print()
        print(f"{Colors.BRIGHT_BLUE}┌{'─' * 78}┐{Colors.RESET}")
        print(f"{Colors.BRIGHT_BLUE}│{Colors.RESET} {Colors.BOLD}🔑 SOFTWARE LICENSES{Colors.RESET}{' ' * 56} {Colors.BRIGHT_BLUE}│{Colors.RESET}")
        print(f"{Colors.BRIGHT_BLUE}└{'─' * 78}┘{Colors.RESET}\n")
        
        print(f"  {Colors.BRIGHT_WHITE}Total Licenses:{Colors.RESET} {Colors.BOLD}{Colors.BRIGHT_CYAN}{stats.get('Licenses', 0)}{Colors.RESET}")
        print(f"  {Colors.BRIGHT_WHITE}Total Seats:{Colors.RESET} {Colors.BOLD}{Colors.BRIGHT_CYAN}{total_license_seats}{Colors.RESET}")
        
        if licenses and total_license_seats > 0:
            used_pct = (used_license_seats / total_license_seats * 100) if total_license_seats > 0 else 0
            available_seats = total_license_seats - used_license_seats
            available_pct = 100 - used_pct
            
            print(f"\n  {Colors.BRIGHT_RED}├─ Used Seats:{Colors.RESET} {used_license_seats} {Colors.DIM}({used_pct:.1f}%){Colors.RESET}")
            self._print_progress_bar(used_pct, 50, Colors.BRIGHT_RED)
            
            print(f"\n  {Colors.BRIGHT_GREEN}└─ Available Seats:{Colors.RESET} {available_seats} {Colors.DIM}({available_pct:.1f}%){Colors.RESET}")
            self._print_progress_bar(available_pct, 50, Colors.BRIGHT_GREEN)
        
        print()
        
        print(f"{Colors.BRIGHT_MAGENTA}┌{'─' * 78}┐{Colors.RESET}")
        print(f"{Colors.BRIGHT_MAGENTA}│{Colors.RESET} {Colors.BOLD}👥 USER STATISTICS{Colors.RESET}{' ' * 58} {Colors.BRIGHT_MAGENTA}│{Colors.RESET}")
        print(f"{Colors.BRIGHT_MAGENTA}└{'─' * 78}┘{Colors.RESET}\n")
        
        total_users = stats.get('Users', 0)
        print(f"  {Colors.BRIGHT_WHITE}Total Users:{Colors.RESET} {Colors.BOLD}{Colors.BRIGHT_CYAN}{total_users}{Colors.RESET}")
        
        if users and total_users > 0:
            active_pct = (active_users / total_users * 100) if total_users > 0 else 0
            users_with_assets_pct = (users_with_assets / total_users * 100) if total_users > 0 else 0
            
            print(f"\n  {Colors.BRIGHT_GREEN}├─ Active Users:{Colors.RESET} {active_users} {Colors.DIM}({active_pct:.1f}%){Colors.RESET}")
            self._print_progress_bar(active_pct, 50, Colors.BRIGHT_GREEN)
            
            print(f"\n  {Colors.BRIGHT_YELLOW}└─ Users with Assets:{Colors.RESET} {users_with_assets} {Colors.DIM}({users_with_assets_pct:.1f}%){Colors.RESET}")
            self._print_progress_bar(users_with_assets_pct, 50, Colors.BRIGHT_YELLOW)
        
        print()
        
        print(f"{Colors.BRIGHT_YELLOW}┌{'─' * 78}┐{Colors.RESET}")
        print(f"{Colors.BRIGHT_YELLOW}│{Colors.RESET} {Colors.BOLD}🏢 ORGANIZATION{Colors.RESET}{' ' * 61} {Colors.BRIGHT_YELLOW}│{Colors.RESET}")
        print(f"{Colors.BRIGHT_YELLOW}└{'─' * 78}┘{Colors.RESET}\n")
        
        org_stats = [
            ('🏷️  Categories', stats.get('Categories', 0), Colors.BRIGHT_CYAN),
            ('🏢 Locations', stats.get('Locations', 0), Colors.BRIGHT_MAGENTA),
            ('🔧 Models', stats.get('Models', 0), Colors.BRIGHT_GREEN),
        ]
        
        for icon_name, count, color in org_stats:
            print(f"  {color}├─{Colors.RESET} {icon_name:.<40} {Colors.BOLD}{color}{count:>5}{Colors.RESET}")
        
        print()
        
        print(f"{Colors.BRIGHT_CYAN}{'═' * 80}{Colors.RESET}")
        print(f"{Colors.BRIGHT_CYAN}║{Colors.RESET} {Colors.BOLD}KEY METRICS SUMMARY{Colors.RESET}{' ' * 59} {Colors.BRIGHT_CYAN}║{Colors.RESET}")
        print(f"{Colors.BRIGHT_CYAN}{'═' * 80}{Colors.RESET}\n")
        
        metrics = [
            ('Asset Utilization', f"{deployed_pct:.1f}%", Colors.BRIGHT_GREEN if deployed_pct > 70 else Colors.BRIGHT_YELLOW),
            ('License Usage', f"{used_pct:.1f}%", Colors.BRIGHT_RED if used_pct > 80 else Colors.BRIGHT_GREEN),
            ('User Activation', f"{active_pct:.1f}%", Colors.BRIGHT_GREEN if active_pct > 90 else Colors.BRIGHT_YELLOW),
            ('Asset Distribution', f"{users_with_assets_pct:.1f}%", Colors.BRIGHT_CYAN),
        ]
        
        for i in range(0, len(metrics), 2):
            left_metric = metrics[i]
            right_metric = metrics[i+1] if i+1 < len(metrics) else None
            
            # Left card
            print(f"  {left_metric[2]}╔═══════════════════════════════════╗{Colors.RESET}", end="")
            if right_metric:
                print(f"  {right_metric[2]}╔═══════════════════════════════════╗{Colors.RESET}")
            else:
                print()
            
            print(f"  {left_metric[2]}║{Colors.RESET} {Colors.BOLD}{left_metric[0][:33].center(33)}{Colors.RESET} {left_metric[2]}║{Colors.RESET}", end="")
            if right_metric:
                print(f"  {right_metric[2]}║{Colors.RESET} {Colors.BOLD}{right_metric[0][:33].center(33)}{Colors.RESET} {right_metric[2]}║{Colors.RESET}")
            else:
                print()
            print(f"  {left_metric[2]}║{Colors.RESET} {Colors.BOLD}{Colors.BRIGHT_WHITE}{left_metric[1].center(33)}{Colors.RESET} {left_metric[2]}║{Colors.RESET}", end="")
            if right_metric:
                print(f"  {right_metric[2]}║{Colors.RESET} {Colors.BOLD}{Colors.BRIGHT_WHITE}{right_metric[1].center(33)}{Colors.RESET} {right_metric[2]}║{Colors.RESET}")
            else:
                print()
            print(f"  {left_metric[2]}╚═══════════════════════════════════╝{Colors.RESET}", end="")
            if right_metric:
                print(f"  {right_metric[2]}╚═══════════════════════════════════╝{Colors.RESET}")
            else:
                print()
            print()
        
        overall_health = (deployed_pct + (100 - used_pct) + active_pct) / 3
        health_color = Colors.BRIGHT_GREEN if overall_health > 70 else Colors.BRIGHT_YELLOW if overall_health > 50 else Colors.BRIGHT_RED
        health_icon = "🟢" if overall_health > 70 else "🟡" if overall_health > 50 else "🔴"
        
        print(f"{health_color}┌{'─' * 78}┐{Colors.RESET}")
        print(f"{health_color}│{Colors.RESET} {health_icon} {Colors.BOLD}OVERALL SYSTEM HEALTH: {overall_health:.1f}%{Colors.RESET}{' ' * (78 - len(f'OVERALL SYSTEM HEALTH: {overall_health:.1f}%') - 4)} {health_color}│{Colors.RESET}")
        print(f"{health_color}└{'─' * 78}┘{Colors.RESET}")
        
        print(f"\n{Colors.BRIGHT_CYAN}{'═' * 80}{Colors.RESET}\n")
        
        UI.print_success("Advanced statistics generated successfully!")
        UI.pause()
    
    def _print_progress_bar(self, percentage: float, width: int = 50, color=Colors.BRIGHT_GREEN):
        filled = int(width * percentage / 100)
        empty = width - filled
        
        bar = f"{color}{'█' * filled}{Colors.DIM}{'░' * empty}{Colors.RESET}"
        print(f"    [{bar}]")

    
    def search_everything(self):
        UI.clear_screen()
        UI.print_header()
        UI.print_box("Universal Search", ["Search across all Snipe-IT resources"], Colors.BRIGHT_MAGENTA)
        
        search_term = UI.get_input("Enter search term").lower()
        
        if not search_term:
            UI.print_warning("Search term cannot be empty!")
            UI.pause()
            return
        
        UI.print_info(f"Searching for '{search_term}'...")
        
        results_found = False
        assets = self.client.list_assets(limit=100)
        if assets:
            matching_assets = [
                a for a in assets 
                if search_term in str(a.get('name', '')).lower() 
                or search_term in str(a.get('asset_tag', '')).lower()
            ]
            if matching_assets:
                results_found = True
                headers = ["ID", "Asset Tag", "Name", "Model"]
                rows = [[a.get('id'), a.get('asset_tag'), a.get('name'), 
                        a.get('model', {}).get('name', 'N/A')] for a in matching_assets]
                UI.print_table(headers, rows, f"📦 MATCHING ASSETS ({len(matching_assets)})")
        
        licenses = self.client.list_licenses(limit=100)
        if licenses:
            matching_licenses = [
                l for l in licenses 
                if search_term in str(l.get('name', '')).lower()
            ]
            if matching_licenses:
                results_found = True
                headers = ["ID", "Name", "Seats"]
                rows = [[l.get('id'), l.get('name'), l.get('seats')] for l in matching_licenses]
                UI.print_table(headers, rows, f"🔑 MATCHING LICENSES ({len(matching_licenses)})")
        
        users = self.client.list_users(limit=100)
        if users:
            matching_users = [
                u for u in users 
                if search_term in str(u.get('username', '')).lower() 
                or search_term in str(u.get('first_name', '')).lower()
                or search_term in str(u.get('last_name', '')).lower()
            ]
            if matching_users:
                results_found = True
                headers = ["ID", "Username", "Name", "Email"]
                rows = [[u.get('id'), u.get('username'), 
                        f"{u.get('first_name', '')} {u.get('last_name', '')}", 
                        u.get('email')] for u in matching_users]
                UI.print_table(headers, rows, f"👥 MATCHING USERS ({len(matching_users)})")
        
        if not results_found:
            UI.print_warning(f"No results found for '{search_term}'")
        else:
            UI.print_success("Search completed!")
        
        UI.pause()
    
    def realtime_monitor(self):
        UI.clear_screen()
        UI.print_header()
        
        print(f"{Colors.BRIGHT_GREEN}┌{'─' * 78}┐{Colors.RESET}")
        print(f"{Colors.BRIGHT_GREEN}│{Colors.RESET} {Colors.BOLD}📡 REAL-TIME MONITORING DASHBOARD{Colors.RESET}{' ' * 43} {Colors.BRIGHT_GREEN}│{Colors.RESET}")
        print(f"{Colors.BRIGHT_GREEN}└{'─' * 78}┘{Colors.RESET}\n")
        
        print(f"{Colors.BRIGHT_CYAN}ℹ Real-time monitoring will check for changes every 5 seconds{Colors.RESET}")
        print(f"{Colors.BRIGHT_CYAN}ℹ Press Ctrl+C to stop monitoring and return to menu{Colors.RESET}\n")
        interval_input = UI.get_input("Refresh interval in seconds (default: 5, min: 3)")
        try:
            refresh_interval = max(3, int(interval_input)) if interval_input else 5
        except ValueError:
            refresh_interval = 5
        
        print(f"\n{Colors.BRIGHT_YELLOW}⚡ Starting real-time monitor with {refresh_interval}s refresh interval...{Colors.RESET}\n")
        time.sleep(1)
        print(f"{Colors.BRIGHT_CYAN}ℹ Establishing baseline data...{Colors.RESET}")
        previous_stats = {
            'assets': self.client.list_assets(limit=500, silent=True) or [],
            'licenses': self.client.list_licenses(limit=500, silent=True) or [],
            'users': self.client.list_users(limit=500, silent=True) or [],
        }
        
        previous_counts = {
            'assets': len(previous_stats['assets']),
            'licenses': len(previous_stats['licenses']),
            'users': len(previous_stats['users']),
        }
        
        print(f"{Colors.BRIGHT_GREEN}✓ Baseline established!{Colors.RESET}")
        print(f"{Colors.DIM}  Assets: {previous_counts['assets']} | Licenses: {previous_counts['licenses']} | Users: {previous_counts['users']}{Colors.RESET}\n")
        print(f"{Colors.BRIGHT_CYAN}{'═' * 80}{Colors.RESET}")
        print(f"{Colors.BRIGHT_CYAN}║{Colors.RESET} {Colors.BOLD}MONITORING ACTIVITY{Colors.RESET}{' ' * 59} {Colors.BRIGHT_CYAN}║{Colors.RESET}")
        print(f"{Colors.BRIGHT_CYAN}{'═' * 80}{Colors.RESET}\n")
        
        iteration = 0
        total_changes = 0
        
        try:
            while True:
                iteration += 1
                current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                
                # Fetch current data silently
                current_stats = {
                    'assets': self.client.list_assets(limit=500, silent=True) or [],
                    'licenses': self.client.list_licenses(limit=500, silent=True) or [],
                    'users': self.client.list_users(limit=500, silent=True) or [],
                }
                
                current_counts = {
                    'assets': len(current_stats['assets']),
                    'licenses': len(current_stats['licenses']),
                    'users': len(current_stats['users']),
                }
                
                changes_detected = False
                
                previous_asset_ids = {a.get('id') for a in previous_stats['assets'] if a.get('id')}
                current_asset_ids = {a.get('id') for a in current_stats['assets'] if a.get('id')}
                
                new_assets = current_asset_ids - previous_asset_ids
                deleted_assets = previous_asset_ids - current_asset_ids
                
                previous_license_ids = {l.get('id') for l in previous_stats['licenses'] if l.get('id')}
                current_license_ids = {l.get('id') for l in current_stats['licenses'] if l.get('id')}
                
                new_licenses = current_license_ids - previous_license_ids
                deleted_licenses = previous_license_ids - current_license_ids
                
                previous_user_ids = {u.get('id') for u in previous_stats['users'] if u.get('id')}
                current_user_ids = {u.get('id') for u in current_stats['users'] if u.get('id')}
                
                new_users = current_user_ids - previous_user_ids
                deleted_users = previous_user_ids - current_user_ids
                
                asset_changes = []
                for current_asset in current_stats['assets']:
                    asset_id = current_asset.get('id')
                    if not asset_id:
                        continue
                        
                    previous_asset = next((a for a in previous_stats['assets'] if a.get('id') == asset_id), None)
                    
                    if previous_asset:
                        prev_status = previous_asset.get('status_label', {}).get('name', 'N/A') if isinstance(previous_asset.get('status_label'), dict) else 'N/A'
                        curr_status = current_asset.get('status_label', {}).get('name', 'N/A') if isinstance(current_asset.get('status_label'), dict) else 'N/A'
                        
                        if prev_status != curr_status:
                            asset_changes.append({
                                'id': asset_id,
                                'name': current_asset.get('name', 'N/A'),
                                'type': 'status',
                                'from': prev_status,
                                'to': curr_status,
                            })
                        
                        prev_assigned = previous_asset.get('assigned_to', {}).get('name') if isinstance(previous_asset.get('assigned_to'), dict) else None
                        curr_assigned = current_asset.get('assigned_to', {}).get('name') if isinstance(current_asset.get('assigned_to'), dict) else None
                        
                        if prev_assigned != curr_assigned:
                            asset_changes.append({
                                'id': asset_id,
                                'name': current_asset.get('name', 'N/A'),
                                'type': 'assignment',
                                'from': prev_assigned or 'Unassigned',
                                'to': curr_assigned or 'Unassigned',
                            })
                
                if new_assets or deleted_assets or new_licenses or deleted_licenses or new_users or deleted_users or asset_changes:
                    changes_detected = True
                    total_changes += 1
                    
                    print(f"\r{' ' * 80}\r", end='')
                    
                    print(f"{Colors.BRIGHT_YELLOW}┌{'─' * 78}┐{Colors.RESET}")
                    print(f"{Colors.BRIGHT_YELLOW}│{Colors.RESET} {Colors.BOLD}🔔 CHANGES DETECTED{Colors.RESET} - {current_time}{' ' * (78 - len(current_time) - 21)} {Colors.BRIGHT_YELLOW}│{Colors.RESET}")
                    print(f"{Colors.BRIGHT_YELLOW}└{'─' * 78}┘{Colors.RESET}\n")
                    
                    if new_assets:
                        print(f"{Colors.BRIGHT_GREEN}  ➕ NEW ASSETS ({len(new_assets)}):{Colors.RESET}")
                        for asset_id in new_assets:
                            asset = next((a for a in current_stats['assets'] if a.get('id') == asset_id), None)
                            if asset:
                                asset_tag = asset.get('asset_tag', 'N/A')
                                asset_name = asset.get('name', 'N/A')
                                model_name = asset.get('model', {}).get('name', 'N/A') if isinstance(asset.get('model'), dict) else 'N/A'
                                print(f"     • ID: {asset_id} | Tag: {asset_tag} | Name: {asset_name} | Model: {model_name}")
                        print()
                    
                    if deleted_assets:
                        print(f"{Colors.BRIGHT_RED}  ➖ DELETED ASSETS ({len(deleted_assets)}):{Colors.RESET}")
                        for asset_id in deleted_assets:
                            asset = next((a for a in previous_stats['assets'] if a.get('id') == asset_id), None)
                            if asset:
                                print(f"     • ID: {asset_id} | Name: {asset.get('name', 'N/A')} | Tag: {asset.get('asset_tag', 'N/A')}")
                        print()
                    
                    if asset_changes:
                        print(f"{Colors.BRIGHT_CYAN}  🔄 ASSET CHANGES ({len(asset_changes)}):{Colors.RESET}")
                        for change in asset_changes:
                            if change.get('type') == 'assignment':
                                print(f"     • {change['name']} (ID: {change['id']})")
                                print(f"       Assignment: {change['from']} → {change['to']}")
                            else:
                                print(f"     • {change['name']} (ID: {change['id']})")
                                print(f"       Status: {change['from']} → {change['to']}")
                        print()
                    
                    if new_licenses:
                        print(f"{Colors.BRIGHT_GREEN}  ➕ NEW LICENSES ({len(new_licenses)}):{Colors.RESET}")
                        for license_id in new_licenses:
                            license_data = next((l for l in current_stats['licenses'] if l.get('id') == license_id), None)
                            if license_data:
                                print(f"     • ID: {license_id} | Name: {license_data.get('name', 'N/A')} | Seats: {license_data.get('seats', 0)}")
                        print()
                    
                    if deleted_licenses:
                        print(f"{Colors.BRIGHT_RED}  ➖ DELETED LICENSES ({len(deleted_licenses)}):{Colors.RESET}")
                        for license_id in deleted_licenses:
                            license_data = next((l for l in previous_stats['licenses'] if l.get('id') == license_id), None)
                            if license_data:
                                print(f"     • ID: {license_id} | Name: {license_data.get('name', 'N/A')}")
                        print()
                    
                    if new_users:
                        print(f"{Colors.BRIGHT_GREEN}  ➕ NEW USERS ({len(new_users)}):{Colors.RESET}")
                        for user_id in new_users:
                            user = next((u for u in current_stats['users'] if u.get('id') == user_id), None)
                            if user:
                                print(f"     • ID: {user_id} | Username: {user.get('username', 'N/A')} | Name: {user.get('first_name', '')} {user.get('last_name', '')}")
                        print()
                    
                    if deleted_users:
                        print(f"{Colors.BRIGHT_RED}  ➖ DELETED USERS ({len(deleted_users)}):{Colors.RESET}")
                        for user_id in deleted_users:
                            user = next((u for u in previous_stats['users'] if u.get('id') == user_id), None)
                            if user:
                                print(f"     • ID: {user_id} | Username: {user.get('username', 'N/A')}")
                        print()
                    
                    print(f"{Colors.DIM}{'─' * 80}{Colors.RESET}\n")
                else:
                    status = f"[{current_time}] Scan #{iteration} - No changes | Assets: {current_counts['assets']} | Licenses: {current_counts['licenses']} | Users: {current_counts['users']} | Total events: {total_changes}"
                    print(f"\r{Colors.DIM}{status[:80]}{Colors.RESET}", end='', flush=True)
                
                previous_stats = current_stats
                previous_counts = current_counts
                
                time.sleep(refresh_interval)
                
        except KeyboardInterrupt:
            print(f"\n\n{Colors.BRIGHT_YELLOW}⚠ Monitoring stopped by user{Colors.RESET}")
            print(f"{Colors.BRIGHT_CYAN}ℹ Total scans performed: {iteration}{Colors.RESET}")
            print(f"{Colors.BRIGHT_CYAN}ℹ Total monitoring time: {iteration * refresh_interval} seconds ({(iteration * refresh_interval) / 60:.1f} minutes){Colors.RESET}")
            print(f"{Colors.BRIGHT_CYAN}ℹ Total change events detected: {total_changes}{Colors.RESET}\n")
            UI.pause()
    
    def exit_application(self):
        UI.clear_screen()
        print(f"\n{Colors.BRIGHT_CYAN}╔════════════════════════════════════════════╗{Colors.RESET}")
        print(f"{Colors.BRIGHT_CYAN}║{Colors.RESET}     {Colors.BOLD}Thank you for using{Colors.RESET}               {Colors.BRIGHT_CYAN}║{Colors.RESET}")
        print(f"{Colors.BRIGHT_CYAN}║{Colors.RESET}     {Colors.BOLD}Snipe-IT Cli Tools!{Colors.RESET}        {Colors.BRIGHT_CYAN}║{Colors.RESET}")
        print(f"{Colors.BRIGHT_CYAN}╚════════════════════════════════════════════╝{Colors.RESET}\n")
        sys.exit(0)

def main():
    try:
        manager = SnipeITManager()
        manager.run()
    except KeyboardInterrupt:
        print(f"\n\n{Colors.BRIGHT_YELLOW}⚠ Application interrupted by user{Colors.RESET}")
        sys.exit(0)
    except Exception as e:
        print(f"\n{Colors.BRIGHT_RED}✗ Fatal Error: {str(e)}{Colors.RESET}")
        sys.exit(1)

if __name__ == "__main__":
    main()
