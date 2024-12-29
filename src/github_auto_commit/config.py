"""Configuration management for GitHub Auto Commit."""

import os
import json
from pathlib import Path
from typing import Dict, Any, Optional

class Config:
    """Manages configuration for GitHub Auto Commit."""
    
    def __init__(self):
        """Initialize configuration."""
        self.config_dir = Path.home() / '.github-auto-commit'
        self.config_file = self.config_dir / 'config.json'
        self.create_config_dir()
        self.load_config()

    def create_config_dir(self) -> None:
        """Create configuration directory if it doesn't exist."""
        self.config_dir.mkdir(parents=True, exist_ok=True)

    def load_config(self) -> None:
        """Load configuration from file."""
        if self.config_file.exists():
            with open(self.config_file, 'r') as f:
                self.config = json.load(f)
        else:
            self.config = {
                'github_token': '',
                'github_username': '',
                'commit_messages': [
                    'Update documentation',
                    'Fix typo',
                    'Update README',
                    'Add new feature',
                    'Fix bug',
                    'Improve performance',
                    'Update dependencies',
                    'Refactor code',
                    'Add tests',
                    'Update CI/CD'
                ]
            }
            self.save_config()

    def save_config(self) -> None:
        """Save configuration to file."""
        with open(self.config_file, 'w') as f:
            json.dump(self.config, f, indent=4)

    def get(self, key: str) -> Any:
        """Get configuration value."""
        return self.config.get(key)

    def set(self, key: str, value: Any) -> None:
        """Set configuration value."""
        self.config[key] = value
        self.save_config()

    def backup(self, backup_file: Optional[str] = None) -> str:
        """Backup configuration to file."""
        if not backup_file:
            backup_file = str(self.config_dir / 'config_backup.json')
        with open(backup_file, 'w') as f:
            json.dump(self.config, f, indent=4)
        return backup_file

    def restore(self, backup_file: str) -> None:
        """Restore configuration from backup."""
        with open(backup_file, 'r') as f:
            self.config = json.load(f)
        self.save_config()

    def reset(self) -> None:
        """Reset configuration to defaults."""
        if self.config_file.exists():
            self.config_file.unlink()
        self.load_config()
