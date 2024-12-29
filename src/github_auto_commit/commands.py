"""Command implementations for GitHub Auto Commit."""

import click
from rich.console import Console
import questionary
from rich.table import Table
from rich.panel import Panel

from .config import Config
from .auto_commit import GitHubAutoCommit

console = Console()

@click.command()
def setup_command():
    """Configure GitHub credentials."""
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
    
    console.print("\n[green]✓ Configuration saved successfully![/green]")

@click.command()
def quick_commit_command():
    """Make a quick commit."""
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

@click.command()
def scheduled_commit_command():
    """Schedule automated commits."""
    config = Config()
    auto_commit = GitHubAutoCommit(config)
    
    frequency = questionary.select(
        "Select commit frequency:",
        choices=[
            "Hourly",
            "Daily",
            "Weekly",
            "Custom"
        ]
    ).ask()
    
    if frequency == "Custom":
        cron = questionary.text(
            "Enter cron expression (e.g., '0 9 * * *' for daily at 9 AM):",
            validate=lambda x: len(x) > 0
        ).ask()
    else:
        cron_map = {
            "Hourly": "0 * * * *",
            "Daily": "0 9 * * *",
            "Weekly": "0 9 * * MON"
        }
        cron = cron_map[frequency]
    
    count = questionary.text(
        "How many commits per run?",
        default="1",
        validate=lambda x: x.isdigit() and int(x) > 0
    ).ask()
    
    console.print(f"\n[green]✓ Scheduled {count} commits {frequency.lower()}![/green]")
    console.print(f"[cyan]Cron expression: {cron}[/cyan]")

@click.command()
def bulk_commit_command():
    """Make multiple commits in bulk."""
    config = Config()
    auto_commit = GitHubAutoCommit(config)
    
    total = questionary.text(
        "Total number of commits:",
        validate=lambda x: x.isdigit() and int(x) > 0
    ).ask()
    
    days = questionary.text(
        "Spread over how many days?",
        validate=lambda x: x.isdigit() and int(x) > 0
    ).ask()
    
    pattern = questionary.select(
        "Distribution pattern:",
        choices=[
            "Even",
            "Random",
            "Front-loaded",
            "Back-loaded"
        ]
    ).ask()
    
    dry_run = questionary.confirm(
        "Would you like to do a dry run first?",
        default=True
    ).ask()
    
    console.print(f"\n[green]✓ Bulk commit plan created![/green]")
    console.print(f"[cyan]• {total} commits over {days} days[/cyan]")
    console.print(f"[cyan]• {pattern} distribution[/cyan]")

@click.command()
def customize_messages():
    """Customize commit messages."""
    config = Config()
    
    while True:
        messages = config.get('commit_messages', [])
        
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

@click.command()
def stats_command():
    """Show contribution statistics."""
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

@click.command()
def show_help():
    """Show help information."""
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

⏰ [bold cyan]Scheduled Commit[/bold cyan]
   Set up automated commit schedules:
   - Hourly, Daily, or Weekly options
   - Custom cron expressions
   - Multiple commits per run

📦 [bold cyan]Bulk Commit[/bold cyan]
   Plan and execute multiple commits:
   - Spread commits over time
   - Choose distribution patterns
   - Preview before execution

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
