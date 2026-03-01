#!/usr/bin/env python3
# ============================================
# WEBSITE CHECKER TOOL - PYTHON VERSION
# ============================================
# Developer: Md. Mainul Islam
# Owner: MAINUL - X
# GitHub: M41NUL
# WhatsApp: +8801308850528
# ============================================

import os
import sys
import time
import socket
import requests
import subprocess
from datetime import datetime

# Rich imports
try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.table import Table
    from rich import box
    from rich.prompt import Prompt
    from rich.align import Align
    from rich.progress import Progress, SpinnerColumn, TextColumn
    from rich.text import Text
    from rich.columns import Columns
    console = Console()
except ImportError:
    os.system("pip install rich")
    from rich.console import Console
    from rich.panel import Panel
    from rich.table import Table
    from rich.prompt import Prompt
    from rich.align import Align
    console = Console()

# PyFiglet
try:
    import pyfiglet
except ImportError:
    os.system("pip install pyfiglet")
    import pyfiglet

class WebsiteChecker:
    def __init__(self):
        self.version = "2.0.0"
        self.developer = "Md. Mainul Islam"
        self.owner = "MAINUL - X"
        self.contact = "+8801308850528"
        self.github = "M41NUL"
        
    def clear_screen(self):
        os.system('clear' if os.name == 'posix' else 'cls')
    
    def show_banner(self):
        self.clear_screen()
        
        # PyFiglet Banner
        banner = pyfiglet.figlet_format("WEB CHECKER", font="slant")
        console.print(Align.center(f"[bold cyan]{banner}[/bold cyan]"))
        console.print(Align.center("[bold bright_yellow]Website Analysis Tool[/bold bright_yellow]"))
        console.print(Align.center(f"[bold green]Version {self.version} | by MAINUL - X[/bold green]"))
        print()
        
        # Developer Info
        info_panel = Panel(
            f"[bold white]Developer:[/bold white] [bold cyan]{self.developer}[/bold cyan]\n"
            f"[bold white]Contact:[/bold white] [bold yellow]{self.contact}[/bold yellow]\n"
            f"[bold white]GitHub:[/bold white] [bold blue]{self.github}[/bold blue]",
            title="[bold white]⚡ MAINUL - X ⚡[/bold white]",
            border_style="bright_cyan",
            box=box.ROUNDED
        )
        console.print(Align.center(info_panel))
        print()
    
    def show_menu(self):
        menu = Panel(
            "[bold cyan]1.[/bold cyan]  Check Website Status (UP/DOWN)\n"
            "[bold cyan]2.[/bold cyan]  Get Website IP Address\n"
            "[bold cyan]3.[bold cyan]  Response Time Test\n"
            "[bold cyan]4.[/bold cyan]  HTTP Headers Info\n"
            "[bold cyan]5.[/bold cyan]  DNS Records (A, MX, NS)\n"
            "[bold cyan]6.[/bold cyan]  Port Scanner\n"
            "[bold cyan]7.[/bold cyan]  SSL Certificate Info\n"
            "[bold cyan]8.[/bold cyan]  WHOIS Lookup\n"
            "[bold cyan]9.[/bold cyan]  Check Multiple Sites\n"
            "[bold red]0.[/bold red]  Exit",
            title="[bold white]📋 MAIN MENU[/bold white]",
            border_style="bright_yellow",
            box=box.ROUNDED
        )
        console.print(Align.center(menu))
        print()
    
    def get_ip(self, site):
        try:
            return socket.gethostbyname(site)
        except:
            return None
    
    def check_status(self, site):
        try:
            response = requests.get(f"http://{site}", timeout=5)
            return True, response.status_code
        except:
            try:
                response = requests.get(f"https://{site}", timeout=5)
                return True, response.status_code
            except:
                return False, None
    
    def option_1_check_status(self):
        site = Prompt.ask("[bold yellow]Enter website[/bold yellow] (e.g., google.com)")
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            progress.add_task("[cyan]Checking...", total=None)
            status, code = self.check_status(site)
            ip = self.get_ip(site)
        
        if status:
            status_panel = Panel(
                f"[bold green]✓ WEBSITE IS UP[/bold green]\n\n"
                f"[bold white]URL:[/bold white] [cyan]{site}[/cyan]\n"
                f"[bold white]IP:[/bold white] [yellow]{ip}[/yellow]\n"
                f"[bold white]Status Code:[/bold white] [green]{code}[/green]",
                border_style="green"
            )
        else:
            status_panel = Panel(
                f"[bold red]✗ WEBSITE IS DOWN[/bold red]\n\n"
                f"[bold white]URL:[/bold white] [cyan]{site}[/cyan]\n"
                f"[bold white]IP:[/bold white] [yellow]{ip if ip else 'Unknown'}[/yellow]",
                border_style="red"
            )
        
        console.print(Align.center(status_panel))
    
    def option_2_get_ip(self):
        site = Prompt.ask("[bold yellow]Enter website[/bold yellow]")
        ip = self.get_ip(site)
        
        if ip:
            ip_panel = Panel(
                f"[bold white]Website:[/bold white] [cyan]{site}[/cyan]\n"
                f"[bold white]IP Address:[/bold white] [bold green]{ip}[/bold green]",
                border_style="cyan"
            )
        else:
            ip_panel = Panel(
                f"[bold red]Could not resolve IP for {site}[/bold red]",
                border_style="red"
            )
        
        console.print(Align.center(ip_panel))
    
    def option_3_response_time(self):
        site = Prompt.ask("[bold yellow]Enter website[/bold yellow]")
        
        times = []
        for i in range(3):
            try:
                start = time.time()
                requests.get(f"https://{site}", timeout=5)
                end = time.time()
                times.append(round((end - start) * 1000, 2))
            except:
                times.append(None)
        
        table = Table(title=f"[bold cyan]Response Time for {site}[/bold cyan]", box=box.ROUNDED)
        table.add_column("Request", style="bold yellow")
        table.add_column("Time (ms)", style="bold green")
        
        for i, t in enumerate(times, 1):
            if t:
                table.add_row(f"Request {i}", f"{t} ms")
            else:
                table.add_row(f"Request {i}", "[red]Failed[/red]")
        
        if all(t for t in times):
            avg = sum(times) / len(times)
            table.add_row("[bold]Average[/bold]", f"[bold cyan]{avg} ms[/bold cyan]")
        
        console.print(Align.center(table))
    
    def option_4_headers(self):
        site = Prompt.ask("[bold yellow]Enter website[/bold yellow]")
        
        try:
            response = requests.get(f"https://{site}", timeout=5)
            
            table = Table(title=f"[bold cyan]HTTP Headers for {site}[/bold cyan]", box=box.ROUNDED)
            table.add_column("Header", style="bold yellow")
            table.add_column("Value", style="bold green")
            
            for key, value in response.headers.items():
                if len(str(value)) > 50:
                    value = str(value)[:50] + "..."
                table.add_row(key, str(value))
            
            console.print(Align.center(table))
        except:
            console.print("[bold red]Failed to fetch headers[/bold red]")
    
    def option_5_dns(self):
        site = Prompt.ask("[bold yellow]Enter website[/bold yellow]")
        
        try:
            # A Records
            a_records = subprocess.getoutput(f"dig +short A {site}").split('\n')
            
            # MX Records
            mx_records = subprocess.getoutput(f"dig +short MX {site}").split('\n')
            
            # NS Records
            ns_records = subprocess.getoutput(f"dig +short NS {site}").split('\n')
            
            table = Table(title=f"[bold cyan]DNS Records for {site}[/bold cyan]", box=box.ROUNDED)
            table.add_column("Type", style="bold yellow")
            table.add_column("Records", style="bold green")
            
            table.add_row("A Records", "\n".join(a_records[:5]) if a_records[0] else "None")
            table.add_row("MX Records", "\n".join(mx_records[:5]) if mx_records[0] else "None")
            table.add_row("NS Records", "\n".join(ns_records[:5]) if ns_records[0] else "None")
            
            console.print(Align.center(table))
        except:
            console.print("[bold red]Failed to fetch DNS records[/bold red]")
    
    def option_6_port_scan(self):
        site = Prompt.ask("[bold yellow]Enter website[/bold yellow]")
        common_ports = [21, 22, 25, 80, 443, 8080, 3306, 5432]
        
        table = Table(title=f"[bold cyan]Port Scan for {site}[/bold cyan]", box=box.ROUNDED)
        table.add_column("Port", style="bold yellow")
        table.add_column("Service", style="bold cyan")
        table.add_column("Status", style="bold green")
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            task = progress.add_task("[cyan]Scanning ports...", total=len(common_ports))
            
            for port in common_ports:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(1)
                result = sock.connect_ex((self.get_ip(site), port))
                
                service = {
                    21: "FTP", 22: "SSH", 25: "SMTP", 80: "HTTP",
                    443: "HTTPS", 8080: "HTTP-Alt", 3306: "MySQL", 5432: "PostgreSQL"
                }.get(port, "Unknown")
                
                status = "[green]Open[/green]" if result == 0 else "[red]Closed[/red]"
                table.add_row(str(port), service, status)
                
                sock.close()
                progress.update(task, advance=1)
        
        console.print(Align.center(table))
    
    def option_7_ssl(self):
        site = Prompt.ask("[bold yellow]Enter website[/bold yellow]")
        
        try:
            import ssl
            import OpenSSL
            import certifi
            
            cert = ssl.get_server_certificate((site, 443))
            x509 = OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_PEM, cert)
            
            table = Table(title=f"[bold cyan]SSL Certificate for {site}[/bold cyan]", box=box.ROUNDED)
            table.add_column("Field", style="bold yellow")
            table.add_column("Value", style="bold green")
            
            table.add_row("Subject", str(x509.get_subject()))
            table.add_row("Issuer", str(x509.get_issuer()))
            table.add_row("Version", str(x509.get_version()))
            table.add_row("Serial Number", str(x509.get_serial_number()))
            
            not_before = x509.get_notBefore().decode('ascii')
            not_after = x509.get_notAfter().decode('ascii')
            table.add_row("Valid From", not_before)
            table.add_row("Valid Until", not_after)
            
            console.print(Align.center(table))
        except:
            console.print("[bold red]Failed to fetch SSL certificate[/bold red]")
    
    def option_8_whois(self):
        site = Prompt.ask("[bold yellow]Enter website[/bold yellow]")
        
        try:
            import whois
            w = whois.whois(site)
            
            table = Table(title=f"[bold cyan]WHOIS Info for {site}[/bold cyan]", box=box.ROUNDED)
            table.add_column("Field", style="bold yellow")
            table.add_column("Value", style="bold green")
            
            if w.registrar:
                table.add_row("Registrar", w.registrar)
            if w.creation_date:
                table.add_row("Created", str(w.creation_date))
            if w.expiration_date:
                table.add_row("Expires", str(w.expiration_date))
            if w.name_servers:
                table.add_row("Name Servers", "\n".join(w.name_servers[:3]))
            
            console.print(Align.center(table))
        except:
            console.print("[bold red]Failed to fetch WHOIS info[/bold red]")
    
    def option_9_multiple(self):
        sites = Prompt.ask("[bold yellow]Enter websites (comma separated)[/bold yellow]").split(',')
        
        table = Table(title="[bold cyan]Multiple Sites Status[/bold cyan]", box=box.ROUNDED)
        table.add_column("Website", style="bold yellow")
        table.add_column("IP Address", style="bold cyan")
        table.add_column("Status", style="bold green")
        table.add_column("Response Time", style="bold white")
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            task = progress.add_task("[cyan]Checking sites...", total=len(sites))
            
            for site in sites:
                site = site.strip()
                ip = self.get_ip(site)
                
                try:
                    start = time.time()
                    r = requests.get(f"https://{site}", timeout=5)
                    end = time.time()
                    time_ms = round((end - start) * 1000, 2)
                    status = f"[green]{r.status_code}[/green]"
                except:
                    status = "[red]DOWN[/red]"
                    time_ms = "N/A"
                
                table.add_row(site, ip or "Unknown", status, str(time_ms))
                progress.update(task, advance=1)
        
        console.print(Align.center(table))
    
    def run(self):
        while True:
            self.show_banner()
            self.show_menu()
            
            choice = Prompt.ask("[bold green]Enter your choice[/bold green]", 
                               choices=["1","2","3","4","5","6","7","8","9","0"])
            
            if choice == '1':
                self.option_1_check_status()
            elif choice == '2':
                self.option_2_get_ip()
            elif choice == '3':
                self.option_3_response_time()
            elif choice == '4':
                self.option_4_headers()
            elif choice == '5':
                self.option_5_dns()
            elif choice == '6':
                self.option_6_port_scan()
            elif choice == '7':
                self.option_7_ssl()
            elif choice == '8':
                self.option_8_whois()
            elif choice == '9':
                self.option_9_multiple()
            elif choice == '0':
                console.print("[bold cyan]Thank you for using Website Checker Tool![/bold cyan]")
                break
            
            input("\n[bold yellow]Press Enter to continue...[/bold yellow]")

if __name__ == "__main__":
    checker = WebsiteChecker()
    checker.run()
