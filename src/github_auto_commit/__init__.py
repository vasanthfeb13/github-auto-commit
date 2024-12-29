"""GitHub Auto Commit - Automate your GitHub contributions."""

__version__ = "1.1.0"

from .auto_commit import GitHubAutoCommit
from .config import Config

__all__ = ['GitHubAutoCommit', 'Config']
