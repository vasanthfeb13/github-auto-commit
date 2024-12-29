"""GitHub Auto Commit core functionality."""

import os
import random
import time
from datetime import datetime
from pathlib import Path
from typing import List, Optional

import git
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TimeElapsedColumn

class GitHubAutoCommit:
    """Handles GitHub auto-commit functionality."""
    
    def __init__(self, config):
        """Initialize with configuration."""
        self.config = config
        self.repo_dir = Path.cwd()
        self.repo = git.Repo(self.repo_dir)

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
            
            for i in range(count):
                commit_message = message or random.choice(messages)
                if not dry_run:
                    self._make_single_commit(commit_message)
                progress.update(task, advance=1, description=f"Commit {i+1}/{count}: {commit_message}")
                if delay and i < count - 1:
                    time.sleep(delay)

    def _make_single_commit(self, message: str) -> None:
        """Make a single commit with the given message."""
        timestamp_file = self.repo_dir / '.timestamp'
        
        # Create or update timestamp file
        with open(timestamp_file, 'w') as f:
            f.write(datetime.now().isoformat())
        
        # Stage and commit
        self.repo.index.add([str(timestamp_file)])
        self.repo.index.commit(message)
        
        # Push to remote
        try:
            origin = self.repo.remote('origin')
            current = self.repo.active_branch
            
            # Try to push with -u flag to set up tracking
            origin.push([current.name], u=True)
            
        except git.exc.GitCommandError as e:
            if "has no upstream branch" in str(e):
                # If pushing with -u fails, try force setting the upstream
                current.set_tracking_branch(origin.refs[current.name])
                origin.push()
            else:
                raise Exception(f"Failed to push commits: {str(e)}")

    def get_stats(self, days: int = 30) -> dict:
        """Get commit statistics for the specified number of days."""
        current = self.repo.active_branch
        commits = list(self.repo.iter_commits(current.name, max_count=100))
        recent_commits = [c for c in commits if (datetime.now() - datetime.fromtimestamp(c.committed_date)).days <= days]
        
        return {
            'total_commits': len(recent_commits),
            'days_active': len(set(datetime.fromtimestamp(c.committed_date).date() for c in recent_commits)),
            'messages': [c.message.strip() for c in recent_commits[:10]],
            'last_commit': datetime.fromtimestamp(commits[0].committed_date).isoformat() if commits else None
        }
