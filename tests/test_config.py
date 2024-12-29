"""Tests for the GitHub Auto Commit package."""

import os
import tempfile
from pathlib import Path
import pytest
import git
from github_auto_commit.config import Config
from github_auto_commit.auto_commit import GitHubAutoCommit

@pytest.fixture
def temp_git_repo():
    """Create a temporary Git repository for testing."""
    with tempfile.TemporaryDirectory() as temp_dir:
        # Initialize Git repo
        repo = git.Repo.init(temp_dir)
        
        # Create a test file
        test_file = Path(temp_dir) / "test.txt"
        test_file.write_text("test content")
        
        # Add and commit the file
        repo.index.add([str(test_file)])
        repo.index.commit("Initial commit")
        
        # Set up remote
        os.environ["GITHUB_TOKEN"] = "test-token"
        os.environ["GITHUB_USERNAME"] = "test-user"
        
        yield temp_dir

@pytest.fixture
def config():
    """Create a test configuration."""
    with tempfile.TemporaryDirectory() as temp_dir:
        config_dir = Path(temp_dir) / ".github_auto_commit"
        config_dir.mkdir(parents=True)
        config_file = config_dir / "config.json"
        
        # Create Config instance with test directory
        test_config = Config()
        test_config.config_dir = config_dir
        test_config.config_file = config_file
        
        # Set test values
        test_config.set("github_username", "test-user")
        test_config.set("github_token", "test-token")
        
        yield test_config

def test_config_initialization(config):
    """Test configuration initialization."""
    assert config.config_file.exists()
    assert config.get("github_username") == "test-user"
    assert config.get("github_token") == "test-token"

def test_config_default_messages(config):
    """Test default commit messages."""
    messages = config.get("commit_messages")
    assert isinstance(messages, list)
    assert len(messages) > 0
    assert "Update documentation" in messages

def test_config_backup_restore(config):
    """Test configuration backup and restore."""
    # Create custom message
    config.set("commit_messages", ["Test message"])
    
    # Backup
    backup_file = config.backup()
    assert Path(backup_file).exists()
    
    # Change message
    config.set("commit_messages", ["Different message"])
    
    # Restore
    config.restore(backup_file)
    assert config.get("commit_messages") == ["Test message"]

@pytest.mark.skipif(not os.environ.get("GITHUB_TOKEN"), reason="No GitHub token available")
def test_auto_commit_initialization(temp_git_repo, config):
    """Test GitHubAutoCommit initialization."""
    os.chdir(temp_git_repo)
    auto_commit = GitHubAutoCommit(config)
    assert isinstance(auto_commit.repo, git.Repo)

@pytest.mark.skipif(not os.environ.get("GITHUB_TOKEN"), reason="No GitHub token available")
def test_make_single_commit(temp_git_repo, config):
    """Test making a single commit."""
    os.chdir(temp_git_repo)
    auto_commit = GitHubAutoCommit(config)
    
    # Make a commit
    message = "Test commit"
    auto_commit._make_single_commit(message)
    
    # Verify commit
    latest_commit = auto_commit.repo.head.commit
    assert latest_commit.message == message

def test_get_stats(temp_git_repo, config):
    """Test getting commit statistics."""
    os.chdir(temp_git_repo)
    auto_commit = GitHubAutoCommit(config)
    
    stats = auto_commit.get_stats(days=30)
    assert isinstance(stats, dict)
    assert "total_commits" in stats
    assert "days_active" in stats
    assert "average_commits_per_day" in stats
