"""Command-line interface for GitHub Auto Commit."""

import os
import sys
import click
import questionary
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.live import Live
from rich.layout import Layout
from rich.align import Align
import pyfiglet

from . import __version__
from .config import Config
from .auto_commit import GitHubAutoCommit

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
    
    table.add_row("", "Configure GitHub credentials")
    table.add_row("", "Make immediate contributions")
    table.add_row("", "Manage configuration")
    table.add_row("", "Customize commit messages")
    table.add_row("", "View contribution statistics")
    table.add_row("", "Show detailed help")
    table.add_row("", "Exit the application")
    
    return Panel(table, title="Available Commands", border_style="blue")

def interactive_setup():
    """Run interactive setup."""
    config = Config()
    
    console.print("\n[bold cyan]GitHub Configuration[/bold cyan]")
    
    username = questionary.text(
        "Enter your GitHub username:",
        validate=lambda x: len(x) > 0,
    ).ask()
    
    token = questionary.password(
        "Enter your GitHub Personal Access Token:",
        validate=lambda x: len(x) > 0,
    ).ask()
    
    config.set("github_username", username)
    config.set("github_token", token)
    
    console.print("\n[green] Configuration saved successfully![/green]")

def interactive_quick_commit():
    """Run interactive quick commit."""
    config = Config()
    auto_commit = GitHubAutoCommit(config)
    
    count = questionary.text(
        "How many commits would you like to make?",
        validate=lambda x: x.isdigit() and int(x) > 0,
    ).ask()
    
    delay = questionary.text(
        "Delay between commits (in seconds, 0 for no delay):",
        default="0",
        validate=lambda x: x.isdigit(),
    ).ask()
    
    message = questionary.text(
        "Custom commit message (press Enter for random):",
    ).ask()
    
    dry_run = questionary.confirm(
        "Would you like to do a dry run first?",
        default=False,
    ).ask()
    
    auto_commit.make_commits(
        count=int(count),
        delay=int(delay),
        message=message if message else None,
        dry_run=dry_run,
    )

def interactive_stats():
    """Show interactive statistics."""
    config = Config()
    auto_commit = GitHubAutoCommit(config)
    
    days = questionary.text(
        "Number of days to analyze:",
        default="30",
        validate=lambda x: x.isdigit() and int(x) > 0,
    ).ask()
    
    stats = auto_commit.get_stats(days=int(days))
    
    table = Table(title=f"Contribution Statistics (Last {days} days)")
    table.add_column("Metric", style="cyan")
    table.add_column("Value", style="green")
    
    table.add_row("Total Commits", str(stats['total_commits']))
    table.add_row("Active Days", str(stats['days_active']))
    table.add_row("Last Commit", stats['last_commit'] or "N/A")
    
    console.print(Panel(table, border_style="blue"))

def interactive_config():
    """Interactive configuration management."""
    config = Config()
    
    action = questionary.select(
        "Configuration Options:",
        choices=[
            "📤 Backup config",
            "📥 Restore config",
            "🔄 Reset config",
            "🔙 Back"
        ]
    ).ask()
    
    if action == "📤 Backup config":
        backup_file = config.backup()
        console.print(f"\n[green]✓ Configuration backed up to: {backup_file}[/green]")
    
    elif action == "📥 Restore config":
        file_path = questionary.text(
            "Enter backup file path:",
            validate=lambda x: os.path.exists(x),
        ).ask()
        config.restore(file_path)
        console.print("\n[green]✓ Configuration restored successfully![/green]")
    
    elif action == "🔄 Reset config":
        if questionary.confirm("Are you sure? This will reset all settings.").ask():
            config.reset()
            console.print("\n[green]✓ Configuration reset to defaults![/green]")

def interactive_messages():
    """Interactive commit message customization."""
    config = Config()
    
    while True:
        messages = config.get('commit_messages')
        
        table = Table(title="Current Commit Messages")
        table.add_column("#", style="cyan")
        table.add_column("Message", style="green")
        
        for i, msg in enumerate(messages, 1):
            table.add_row(str(i), msg)
        
        console.print(Panel(table, border_style="blue"))
        
        action = questionary.select(
            "Message Options:",
            choices=[
                "➕ Add message",
                "✏️  Edit message",
                "❌ Remove message",
                "🔙 Back"
            ]
        ).ask()
        
        if action == "🔙 Back":
            break
        
        elif action == "➕ Add message":
            new_msg = questionary.text(
                "Enter new commit message:",
                validate=lambda x: len(x) > 0
            ).ask()
            messages.append(new_msg)
            
        elif action == "✏️  Edit message":
            idx = questionary.select(
                "Select message to edit:",
                choices=[f"{i+1}. {msg}" for i, msg in enumerate(messages)]
            ).ask()
            idx = int(idx.split('.')[0]) - 1
            new_msg = questionary.text(
                "Enter new message:",
                default=messages[idx]
            ).ask()
            messages[idx] = new_msg
            
        elif action == "❌ Remove message":
            idx = questionary.select(
                "Select message to remove:",
                choices=[f"{i+1}. {msg}" for i, msg in enumerate(messages)]
            ).ask()
            idx = int(idx.split('.')[0]) - 1
            messages.pop(idx)
        
        config.set('commit_messages', messages)
        console.print("\n[green]✓ Commit messages updated![/green]")

def show_help():
    """Show detailed help information."""
    help_text = """
🔧 [bold cyan]Setup[/bold cyan]
   Configure your GitHub credentials including username and personal access token.
   You'll need to create a token with 'repo' scope from GitHub settings.

🚀 [bold cyan]Quick Commit[/bold cyan]
   Make immediate contributions to your repository.
   - Specify number of commits
   - Set delay between commits
   - Use custom or random commit messages
   - Test with dry run mode

⚙️  [bold cyan]Config[/bold cyan]
   Manage your configuration:
   - Backup current settings
   - Restore from backup
   - Reset to defaults

✏️  [bold cyan]Messages[/bold cyan]
   Customize your commit messages:
   - Add new messages
   - Edit existing messages
   - Remove messages
   - View all current messages

📊 [bold cyan]Stats[/bold cyan]
   View your contribution statistics:
   - Total commits
   - Active days
   - Recent activity
   - Contribution patterns

❓ [bold cyan]Help[/bold cyan]
   Show this help information

🚪 [bold cyan]Exit[/bold cyan]
   Exit the application
"""
    console.print(Panel(help_text, title="Help & Documentation", border_style="blue"))

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
                "⚙️  config",
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
            interactive_setup()
        
        elif choice == "🚀 quick-commit":
            interactive_quick_commit()
        
        elif choice == "📊 stats":
            interactive_stats()
        
        elif choice == "⚙️  config":
            interactive_config()
            
        elif choice == "✏️  messages":
            interactive_messages()
            
        elif choice == "❓ help":
            show_help()
        
        input("\nPress Enter to continue...")
        console.clear()

def main():
    """Main entry point for the CLI."""
    try:
        main_loop()
    except KeyboardInterrupt:
        console.print("\n[yellow]Thanks for using GitHub Auto-Commit! [/yellow]")
        sys.exit(0)
    except Exception as e:
        console.print(f"\n[red]Error: {str(e)}[/red]")
        sys.exit(1)
