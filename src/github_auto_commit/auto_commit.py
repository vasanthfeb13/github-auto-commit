"""GitHub Auto Commit core functionality."""

import os
import random
import time
from datetime import datetime
from pathlib import Path
from typing import List, Optional, Dict, Any

import git
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TimeElapsedColumn

console = Console()

class GitHubAutoCommit:
    """Handles GitHub auto-commit functionality."""
    
    def __init__(self, config):
        """Initialize with configuration."""
        self.config = config
        self.repo_dir = Path.cwd()
        try:
            self.repo = git.Repo(self.repo_dir)
            self._validate_repo()
        except git.exc.InvalidGitRepositoryError:
            raise Exception("Not a valid Git repository. Please run this from a Git repository.")
    
    def _validate_repo(self) -> None:
        """Validate repository configuration."""
        if not self.repo.remotes:
            raise Exception("No remote repository configured. Please add a remote first.")
        
        if not self.config.get('github_username') or not self.config.get('github_token'):
            raise Exception("GitHub credentials not configured. Please run setup first.")

    def make_commits(self, count: int, delay: int = 0, message: Optional[str] = None,
                    dry_run: bool = False) -> None:
        """Make specified number of commits."""
        messages = self.config.get('commit_messages', [
            "Update documentation",
            "Fix typo",
            "Update README",
            "Add new feature",
            "Improve performance",
            "Fix bug",
            "Clean up code",
            "Refactor code",
            "Update dependencies",
            "Add tests"
        ])
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TimeElapsedColumn(),
        ) as progress:
            task = progress.add_task(f"Making {count} commits...", total=count)
            
            try:
                for i in range(count):
                    commit_message = message or random.choice(messages)
                    if not dry_run:
                        self._make_single_commit(commit_message)
                        self._push_commits()
                    progress.update(task, advance=1, description=f"Commit {i+1}/{count}: {commit_message}")
                    if delay and i < count - 1:
                        time.sleep(delay)
                
                if not dry_run:
                    console.print("\n[green]✓ All commits pushed successfully![/green]")
                else:
                    console.print("\n[yellow]Dry run completed. No actual commits were made.[/yellow]")
                    
            except Exception as e:
                console.print(f"\n[red]Error during commit process: {str(e)}[/red]")
                raise

    def _make_single_commit(self, message: str) -> None:
        """Make a single commit with the given message."""
        timestamp_file = self.repo_dir / '.timestamp'
        
        # Create or update timestamp file
        with open(timestamp_file, 'w') as f:
            f.write(datetime.now().isoformat())
        
        # Stage and commit
        self.repo.index.add([str(timestamp_file)])
        self.repo.index.commit(message)

    def _push_commits(self) -> None:
        """Push commits to remote repository."""
        try:
            origin = self.repo.remote('origin')
            current = self.repo.active_branch
            
            # First try to push normally
            try:
                origin.push()
                return
            except git.exc.GitCommandError:
                pass
            
            # If normal push fails, try to set up tracking
            try:
                origin.push([current.name], u=True)
            except git.exc.GitCommandError:
                # If that fails too, try to manually set tracking
                remote_branch = origin.refs[current.name]
                current.set_tracking_branch(remote_branch)
                origin.push()
                
        except Exception as e:
            raise Exception(f"Failed to push commits: {str(e)}")

    def get_stats(self, days: int = 30) -> Dict[str, Any]:
        """Get commit statistics for the specified number of days."""
        try:
            current = self.repo.active_branch
            commits = list(self.repo.iter_commits(current.name, max_count=100))
            recent_commits = [c for c in commits if (datetime.now() - datetime.fromtimestamp(c.committed_date)).days <= days]
            
            active_days = set(datetime.fromtimestamp(c.committed_date).date() for c in recent_commits)
            
            return {
                'total_commits': len(recent_commits),
                'days_active': len(active_days),
                'average_commits_per_day': round(len(recent_commits) / days, 2) if days > 0 else 0,
                'messages': [c.message.strip() for c in recent_commits[:10]],
                'last_commit': datetime.fromtimestamp(commits[0].committed_date).isoformat() if commits else None
            }
        except Exception as e:
            console.print(f"[red]Error getting stats: {str(e)}[/red]")
            return {
                'total_commits': 0,
                'days_active': 0,
                'average_commits_per_day': 0,
                'messages': [],
                'last_commit': None
            }
