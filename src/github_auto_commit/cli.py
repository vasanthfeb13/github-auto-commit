"""Command-line interface for GitHub Auto Commit."""

import os
import sys
import click
import questionary
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
import pyfiglet

from . import __version__
from .config import Config
from .auto_commit import GitHubAutoCommit
from .commands import (
    setup_command,
    quick_commit_command,
    scheduled_commit_command,
    bulk_commit_command,
    customize_messages,
    stats_command,
    show_help
)

console = Console()

def print_banner():
    """Print the application banner."""
    ascii_art = pyfiglet.figlet_format("GitHub Auto-Commit")
    console.print(Panel(
        f"[bold green]{ascii_art}[/bold green]\n"
        "[yellow]A powerful tool for automating GitHub contributions[/yellow]\n"
        f"[cyan]Version: {__version__}[/cyan]",
        title="Welcome",
        border_style="green",
    ))

def create_main_menu():
    """Create the main menu table."""
    table = Table(show_header=False, box=None)
    table.add_column("Command", style="cyan")
    table.add_column("Description", style="white")
    
    table.add_row("🔧 setup", "Configure GitHub credentials")
    table.add_row("🚀 quick-commit", "Make immediate contributions")
    table.add_row("⏰ scheduled", "Schedule automated commits")
    table.add_row("📦 bulk", "Make multiple commits in bulk")
    table.add_row("✏️  messages", "Customize commit messages")
    table.add_row("📊 stats", "View contribution statistics")
    table.add_row("❓ help", "Show detailed help")
    table.add_row("🚪 exit", "Exit the application")
    
    return Panel(table, title="Available Commands", border_style="blue")

def main_loop():
    """Main application loop."""
    while True:
        print_banner()
        console.print(create_main_menu())
        
        choice = questionary.select(
            "What would you like to do?",
            choices=[
                "🔧 setup",
                "🚀 quick-commit",
                "⏰ scheduled",
                "📦 bulk",
                "✏️  messages",
                "📊 stats",
                "❓ help",
                "🚪 exit"
            ],
        ).ask()
        
        if choice == "🚪 exit":
            console.print("\n[yellow]Thanks for using GitHub Auto-Commit! 👋[/yellow]")
            sys.exit(0)
        
        elif choice == "🔧 setup":
            setup_command()
        
        elif choice == "🚀 quick-commit":
            quick_commit_command()
            
        elif choice == "⏰ scheduled":
            scheduled_commit_command()
            
        elif choice == "📦 bulk":
            bulk_commit_command()
        
        elif choice == "✏️  messages":
            customize_messages()
        
        elif choice == "📊 stats":
            stats_command()
            
        elif choice == "❓ help":
            show_help()
        
        input("\nPress Enter to continue...")
        console.clear()

def main():
    """Main entry point for the CLI."""
    try:
        main_loop()
    except KeyboardInterrupt:
        console.print("\n[yellow]Thanks for using GitHub Auto-Commit! 👋[/yellow]")
        sys.exit(0)
    except Exception as e:
        console.print(f"\n[red]Error: {str(e)}[/red]")
        sys.exit(1)
