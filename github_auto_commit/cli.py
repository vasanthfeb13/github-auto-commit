"""Command-line interface for GitHub Auto Commit."""

import click
from rich.console import Console
import pyfiglet

from .config import Config
from .auto_commit import GitHubAutoCommit
from .commands import (
    setup_command,
    quick_commit_command,
    config_command,
    customize_messages,
    show_help,
)

console = Console()

@click.group()
def cli():
    """GitHub Auto Commit - Automate your GitHub contributions."""
    ascii_art = pyfiglet.figlet_format("GitHub Auto-Commit")
    console.print(f"[bold green]{ascii_art}[/bold green]")

cli.add_command(setup_command)
cli.add_command(quick_commit_command)
cli.add_command(config_command)
cli.add_command(customize_messages)
cli.add_command(show_help)

def main():
    """Main entry point for the CLI."""
    cli()
