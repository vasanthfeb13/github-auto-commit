"""Configuration management for GitHub Auto Commit."""

import json
import os
import shutil
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Optional

class Config:
    """Manages configuration settings."""
    
    def __init__(self):
        """Initialize configuration."""
        self.config_dir = Path.home() / '.github_auto_commit'
        self.config_file = self.config_dir / 'config.json'
        self._ensure_config_exists()
        
    def _ensure_config_exists(self):
        """Ensure configuration directory and file exist."""
        self.config_dir.mkdir(parents=True, exist_ok=True)
        if not self.config_file.exists():
            self._save_config(self._get_default_config())
    
    def _get_default_config(self) -> Dict[str, Any]:
        """Get default configuration."""
        return {
            'github_username': '',
            'github_token': '',
            'commit_messages': [
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
            ]
        }
    
    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from file."""
        try:
            with open(self.config_file, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading config: {e}")
            return self._get_default_config()
    
    def _save_config(self, config: Dict[str, Any]):
        """Save configuration to file."""
        with open(self.config_file, 'w') as f:
            json.dump(config, f, indent=4)
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get a configuration value."""
        config = self._load_config()
        return config.get(key, default)
    
    def set(self, key: str, value: Any):
        """Set a configuration value."""
        config = self._load_config()
        config[key] = value
        self._save_config(config)
    
    def reset(self):
        """Reset configuration to defaults."""
        self._save_config(self._get_default_config())
    
    def backup(self) -> str:
        """Backup the configuration file."""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_file = self.config_dir / f'config_backup_{timestamp}.json'
        shutil.copy2(self.config_file, backup_file)
        return str(backup_file)
    
    def restore(self, backup_file: str):
        """Restore configuration from backup."""
        if not os.path.exists(backup_file):
            raise FileNotFoundError(f"Backup file not found: {backup_file}")
        shutil.copy2(backup_file, self.config_file)
