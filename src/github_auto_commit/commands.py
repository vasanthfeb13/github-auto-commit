"""Command implementations for GitHub Auto Commit."""
import os
import json
import time
from pathlib import Path
from datetime import datetime
import click
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn
import questionary

from .config import Config
from .auto_commit import GitHubAutoCommit

console = Console()

@click.command()
@click.option('--username', prompt='GitHub Username')
@click.option('--token', prompt='GitHub Token', hide_input=True)
def setup_command(username, token):
    """Set up GitHub credentials."""
    config = Config()
    config.set_credentials(username, token)
    console.print("[green]✅ Credentials saved successfully![/green]")

@click.command()
@click.option('--message', help='Custom commit message template')
@click.option('--dry-run', is_flag=True, help='Run without making actual commits')
def quick_commit_command(message, dry_run):
    """Make commits immediately."""
    config = Config()
    auto_commit = GitHubAutoCommit()
    
    if not config.config.get('default_repository'):
        console.print("[red]Error: No default repository set. Please set one using 'set-repo' command.[/red]")
        return

    pattern = config.config['contribution_pattern']
    pattern_info = config.config['commit_patterns'][pattern]
    count = click.prompt('Number of commits', type=int, default=pattern_info['min'])

    if message:
        config.config['commit_messages'] = [message]
        config.save()

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TaskProgressColumn(),
        console=console,
    ) as progress:
        task = progress.add_task(f"Making {count} commits...", total=count)
        
        for i in range(count):
            if dry_run:
                console.print(f"[yellow]DRY RUN: Would make commit {i+1} of {count}[/yellow]")
                time.sleep(1)
            else:
                auto_commit.make_contribution()
            progress.update(task, advance=1)
            
            if i < count - 1:
                time.sleep(2)

    if dry_run:
        console.print("\n[yellow]Dry run completed. No actual commits were made.[/yellow]")
    else:
        console.print("\n[green]✅ Quick commits completed successfully![/green]")

@click.command()
@click.option('--backup', is_flag=True, help='Backup current configuration')
@click.option('--restore', type=click.Path(exists=True), help='Restore configuration from backup')
def config_command(backup, restore):
    """Backup or restore configuration."""
    config = Config()
    
    if backup:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_file = f'github_auto_commit_config_{timestamp}.json'
        
        with open(backup_file, 'w') as f:
            json.dump(config.config, f, indent=2)
        
        console.print(f"[green]✅ Configuration backed up to {backup_file}[/green]")
    
    elif restore:
        with open(restore, 'r') as f:
            restored_config = json.load(f)
        
        config.config = restored_config
        config.save()
        console.print("[green]✅ Configuration restored successfully![/green]")

@click.command()
def customize_messages():
    """Customize commit messages."""
    config = Config()
    
    while True:
        action = questionary.select(
            "Choose an action:",
            choices=[
                "View current messages",
                "Add new message",
                "Remove message",
                "Reset to defaults",
                "Done"
            ]
        ).ask()
        
        if action == "View current messages":
            console.print("\nCurrent commit messages:")
            for i, msg in enumerate(config.config['commit_messages'], 1):
                console.print(f"{i}. {msg}")
                
        elif action == "Add new message":
            new_msg = questionary.text("Enter new commit message:").ask()
            if new_msg:
                config.config['commit_messages'].append(new_msg)
                config.save()
                console.print("[green]✅ Message added![/green]")
                
        elif action == "Remove message":
            if len(config.config['commit_messages']) > 1:
                msg_to_remove = questionary.select(
                    "Select message to remove:",
                    choices=config.config['commit_messages']
                ).ask()
                config.config['commit_messages'].remove(msg_to_remove)
                config.save()
                console.print("[green]✅ Message removed![/green]")
            else:
                console.print("[red]Cannot remove the last message![/red]")
                
        elif action == "Reset to defaults":
            config.reset_commit_messages()
            console.print("[green]✅ Messages reset to defaults![/green]")
            
        elif action == "Done":
            break

@click.command()
@click.option('--days', default=30, help='Number of days to analyze')
def stats_command(days):
    """Show contribution statistics and heatmap."""
    config = Config()
    token = os.getenv('GITHUB_TOKEN')
    username = os.getenv('GITHUB_USERNAME')
    
    if not token or not username:
        console.print("[red]Error: GitHub credentials not found. Please run 'setup' first.[/red]")
        return
    
    try:
        stats = ContributionStats(token)
        stats.display_stats(username, days)
    except Exception as e:
        console.print(f"[red]Error fetching statistics: {str(e)}[/red]")

@click.command()
def show_help():
    """Show detailed help and examples."""
    help_text = """
🚀 GitHub Auto Commit Help

Commands:
  setup              Configure GitHub credentials
  quick-commit       Make immediate commits
  config            Backup or restore configuration
  customize-messages Customize commit messages
  start             Start the auto-commit service
  status            Show current configuration
  stats             Show contribution statistics and heatmap

Examples:
  # Make 5 quick commits
  github-auto-commit quick-commit --count 5

  # Dry run to test configuration
  github-auto-commit quick-commit --dry-run

  # Backup configuration
  github-auto-commit config --backup

  # Restore configuration
  github-auto-commit config --restore config_backup.json

  # Customize commit messages
  github-auto-commit customize-messages

  # Show contribution statistics
  github-auto-commit stats

For more information, visit: https://github.com/vasanthfeb13/github-auto-commit
    """
    console.print(help_text)
