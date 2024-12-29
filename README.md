# GitHub Auto Commit 🚀

<div align="center">

[![PyPI version](https://badge.fury.io/py/github-auto-commit.svg)](https://badge.fury.io/py/github-auto-commit)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Versions](https://img.shields.io/pypi/pyversions/github-auto-commit.svg)](https://pypi.org/project/github-auto-commit/)
[![Tests](https://github.com/vasanthfeb13/github-auto-commit/actions/workflows/python-package.yml/badge.svg)](https://github.com/vasanthfeb13/github-auto-commit/actions)
[![Downloads](https://img.shields.io/pypi/dm/github-auto-commit.svg)](https://pypi.org/project/github-auto-commit/)

**A powerful command-line tool for automating GitHub contributions with customizable schedules and patterns.**

[Installation](#-installation) •
[Quick Start](#-quick-start) •
[Features](#-features) •
[Usage Guide](#-usage-guide) •
[Configuration](#️-configuration) •
[Examples](#-examples) •
[FAQ](#-faq)

</div>

## ✨ Features

<details open>
<summary>Click to expand/collapse</summary>

- ⏰ **Flexible Scheduling**: Set custom hours and days for commits
- 📊 **Customizable Patterns**: Choose from preset commit patterns or create your own
- 🔄 **Quick Commits**: Make immediate contributions with progress tracking
- 🎯 **Dry Run Mode**: Test your configuration without making actual commits
- 💾 **Config Backup/Restore**: Easily backup and restore your settings
- 📝 **Custom Messages**: Personalize your commit messages
- 📈 **Statistics**: View contribution stats and activity heatmap
- 🔐 **Secure**: Uses GitHub Personal Access Token for authentication
- 🎨 **User-Friendly**: Interactive CLI with rich progress bars and status updates

</details>

## 📦 Installation

### Prerequisites
- Python 3.8 or higher
- Git installed and configured
- GitHub account

### Via pip (Recommended)
```bash
pip install github-auto-commit
```

### From source
```bash
git clone https://github.com/vasanthfeb13/github-auto-commit.git
cd github-auto-commit
pip install -e .
```

## 🚀 Quick Start

1. **Install the package**
```bash
pip install github-auto-commit
```

2. **Set up GitHub credentials**
```bash
github-auto-commit setup
```

3. **Make your first commits**
```bash
github-auto-commit quick-commit --count 3
```

## 📖 Usage Guide

### Initial Setup

1. **Create a GitHub Personal Access Token**
   - Go to GitHub Settings → Developer Settings → Personal Access Tokens
   - Click "Generate new token (classic)"
   - Select scopes: `repo` and `user`
   - Copy the generated token

2. **Configure the Tool**
```bash
# Interactive setup
github-auto-commit setup

# Or use command-line arguments
github-auto-commit setup --username YOUR_USERNAME --token YOUR_TOKEN
```

### Making Contributions

#### Quick Commits
```bash
# Make 5 commits immediately
github-auto-commit quick-commit --count 5

# Test configuration with dry run
github-auto-commit quick-commit --dry-run

# Custom commit message
github-auto-commit quick-commit --message "Update documentation"
```

#### Customizing Commit Messages
```bash
# Launch interactive message editor
github-auto-commit customize-messages

# View current messages
github-auto-commit customize-messages --show
```

### Configuration Management

#### Backup Your Settings
```bash
# Create backup
github-auto-commit config --backup

# Restore from backup
github-auto-commit config --restore config_backup.json
```

### Statistics and Analytics

```bash
# View last 30 days of contributions
github-auto-commit stats

# Analyze last 90 days
github-auto-commit stats --days 90

# View repository breakdown
github-auto-commit stats --repos
```

The statistics view shows:
- Total commits and active days
- Average commits per day
- Repository breakdown
- Activity heatmap
- Most active days and repositories
- Contribution trends

## ⚙️ Configuration

### Commit Patterns

| Pattern | Commits/Day | Best For |
|---------|------------|----------|
| Light   | 1-2        | Casual contributors |
| Moderate| 2-4        | Regular developers |
| Heavy   | 4-8        | Active maintainers |
| Custom  | You decide | Special needs |

### Schedule Options

| Preset | Hours | Days | Description |
|--------|-------|------|-------------|
| Work Hours | 9AM-5PM | Mon-Fri | Standard work schedule |
| Evening | 6PM-10PM | Mon-Fri | After-hours coding |
| Weekend | 10AM-8PM | Sat-Sun | Weekend warrior |
| Night Owl | 8PM-2AM | Any | Late-night coding |
| Custom | Any | Any | Your preferred schedule |

## 💡 Examples

### Basic Usage

```bash
# Start with quick commits
github-auto-commit quick-commit --count 3

# View your stats
github-auto-commit stats

# Backup configuration
github-auto-commit config --backup
```

### Advanced Usage

```bash
# Custom commit pattern with progress bar
github-auto-commit quick-commit --count 5 --delay 2

# Analyze specific time period
github-auto-commit stats --days 90 --repos

# Dry run with custom message
github-auto-commit quick-commit --dry-run --message "Update docs"

# Interactive commit message customization
github-auto-commit customize-messages
```

## 🤔 FAQ

### Q: Is it safe to use?
**A:** Yes! We use GitHub's official API and secure token authentication. Your credentials are stored locally and securely.

### Q: Will it affect my existing repositories?
**A:** No, it only modifies the repositories you explicitly configure it to work with.

### Q: Can I customize commit messages?
**A:** Yes! Use `github-auto-commit customize-messages` to set your own messages.

### Q: What if I want to stop the service?
**A:** Use `Ctrl+C` to stop the service, or run `github-auto-commit stop`.

### Q: How do I update to the latest version?
**A:** Run `pip install --upgrade github-auto-commit`

## 🔧 Troubleshooting

### Common Issues

1. **Authentication Failed**
   - Ensure your GitHub token has the correct permissions
   - Try regenerating your token
   - Check if token is correctly set in configuration

2. **Rate Limiting**
   - GitHub API has rate limits
   - Try reducing commit frequency
   - Use `--delay` option with quick-commit

3. **Configuration Issues**
   - Run `github-auto-commit config --reset` to start fresh
   - Use `--backup` before making changes
   - Check logs for detailed error messages

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

1. Fork the repository
2. Create your feature branch
3. Make your changes
4. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Thanks to all contributors
- Built with [Rich](https://github.com/Textualize/rich) for beautiful CLI
- Inspired by the GitHub community

## 📞 Support

Need help? Here are some ways to get support:

1. Check the [FAQ](#faq) section
2. Open an [issue](https://github.com/vasanthfeb13/github-auto-commit/issues)
3. follow me on insta (https://www.instagram.com/vasanthadithya_m/)

---

<div align="center">
Made with ❤️ by the GitHub Auto Commit Team
</div>
