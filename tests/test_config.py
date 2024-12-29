"""Tests for the config module."""
import pytest
from github_auto_commit.config import Config

def test_default_config():
    """Test default configuration values."""
    config = Config()
    assert 'commit_patterns' in config.config
    assert 'schedule' in config.config
    assert 'commit_messages' in config.config

def test_commit_patterns():
    """Test commit pattern ranges."""
    config = Config()
    patterns = config.config['commit_patterns']
    
    assert 'light' in patterns
    assert 'moderate' in patterns
    assert 'heavy' in patterns
    
    assert patterns['light']['min'] <= patterns['light']['max']
    assert patterns['moderate']['min'] <= patterns['moderate']['max']
    assert patterns['heavy']['min'] <= patterns['heavy']['max']

def test_schedule():
    """Test schedule configuration."""
    config = Config()
    schedule = config.config['schedule']
    
    assert 0 <= schedule['start_hour'] <= 23
    assert 0 <= schedule['end_hour'] <= 23
    assert isinstance(schedule['days'], list)
    assert all(day in ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'] 
              for day in schedule['days'])
