"""Command-line interface for GitHub Auto Commit."""

import click
from rich.console import Console
import pyfiglet

from .config import Config
from .auto_commit import GitHubAutoCommit
from .commands import (
    setup_command,
    configure_command,
    start_command,
    quick_commit_command,
    set_schedule_command,
    set_frequency_command,
    show_schedule_command,
    show_frequency_command,
    show_help_command,
    status_command,
)

console = Console()

@click.group()
def cli():
    """GitHub Auto Commit - Automate your GitHub contributions."""
    console.print(pyfiglet.figlet_format("GitHub Auto-Commit"))

cli.add_command(setup_command)
cli.add_command(configure_command)
cli.add_command(start_command)
cli.add_command(quick_commit_command)
cli.add_command(set_schedule_command)
cli.add_command(set_frequency_command)
cli.add_command(show_schedule_command)
cli.add_command(show_frequency_command)
cli.add_command(show_help_command)
cli.add_command(status_command)

def main():
    """Main entry point for the CLI."""
    cli()
