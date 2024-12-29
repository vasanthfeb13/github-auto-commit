# GitHub Auto Commit 🚀

A powerful command-line tool for automating GitHub contributions with customizable schedules and patterns.

## Features ✨

- 🕒 **Flexible Scheduling**: Set custom hours and days for commits
- 📊 **Customizable Patterns**: Choose from preset commit patterns or create your own
- 🔄 **Quick Commits**: Make immediate contributions with progress tracking
- 🎯 **Dry Run Mode**: Test your configuration without making actual commits
- 💾 **Config Backup/Restore**: Easily backup and restore your settings
- 📝 **Custom Messages**: Personalize your commit messages
- 🔐 **Secure**: Uses GitHub Personal Access Token for authentication
- 📱 **User-Friendly**: Interactive CLI with rich progress bars and status updates

## Installation 📦

```bash
pip install github-auto-commit
```

## Quick Start 🚀

1. **Setup your GitHub credentials**:
```bash
github-auto-commit setup
```

2. **Make some quick commits**:
```bash
# Make 5 commits
github-auto-commit quick-commit --count 5

# Test with dry run
github-auto-commit quick-commit --dry-run
```

3. **Customize commit messages**:
```bash
github-auto-commit customize-messages
```

## Available Commands 🛠️

- `setup`: Configure GitHub credentials
- `quick-commit`: Make immediate commits
  - `--count`: Number of commits to make
  - `--message`: Custom commit message
  - `--dry-run`: Test without making actual commits
- `config`: Manage configuration
  - `--backup`: Backup current settings
  - `--restore`: Restore from backup
- `customize-messages`: Personalize commit messages
- `help`: Show detailed help

## Configuration Management 📋

### Backup Configuration
```bash
github-auto-commit config --backup
```

### Restore Configuration
```bash
github-auto-commit config --restore config_backup.json
```

### Customize Commit Messages
```bash
github-auto-commit customize-messages
```

## Security 🔒

- Uses GitHub Personal Access Token for authentication
- Credentials stored securely in local .env file
- File permissions restricted to user only

## Contributing 🤝

Contributions are welcome! Please feel free to submit a Pull Request.

## License 📄

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Author ✍️

Created by [Vasanth Adithya](https://github.com/vasanthfeb13)

## Support 💖

If you find this tool helpful, please consider giving it a star ⭐️ on GitHub!
