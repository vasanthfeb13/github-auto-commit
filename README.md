# GitHub Auto Commit 🚀

A powerful CLI tool for automating GitHub contributions with style and flexibility.

![Version](https://img.shields.io/badge/version-1.1.0-blue)
![Python](https://img.shields.io/badge/python-3.8%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)

## ✨ Features

- 🎯 **Multiple Commit Modes**
  - Quick commits for immediate contributions
  - Scheduled commits with customizable intervals
  - Bulk commits with pattern distribution
  
- 🎨 **Interactive CLI**
  - Beautiful command-line interface
  - Rich text output with colors
  - Progress indicators and status messages
  
- ⚙️ **Flexible Configuration**
  - Customizable commit messages
  - Backup and restore settings
  - Secure credential management
  
- 📊 **Statistics & Insights**
  - View contribution patterns
  - Track commit history
  - Monitor activity metrics

## 🚀 Quick Start

### Installation

```bash
pip install github-auto-commit
```

### Initial Setup

1. Create a GitHub Personal Access Token:
   - Go to GitHub Settings → Developer Settings → Personal Access Tokens
   - Generate a new token with 'repo' scope
   - Copy the token for configuration

2. Run the setup command:
```bash
github-auto-commit
```
Select "🔧 Setup" and follow the prompts to configure your credentials.

## 💫 Usage

### Quick Commits

Make immediate contributions:
```bash
github-auto-commit
```
Select "🚀 Quick Commit" and follow the prompts to:
- Set number of commits
- Add delay between commits
- Use custom messages
- Try dry run mode

### Scheduled Commits

Set up automated commit schedules:
```bash
github-auto-commit
```
Select "⏰ Scheduled" to:
- Choose frequency (hourly/daily/weekly)
- Set custom cron expressions
- Configure commit count per run

### Bulk Commits

Plan multiple commits over time:
```bash
github-auto-commit
```
Select "📦 Bulk" to:
- Set total commit count
- Spread over multiple days
- Choose distribution pattern
- Preview before execution

### Customize Messages

Manage your commit messages:
```bash
github-auto-commit
```
Select "✏️ Messages" to:
- Add new messages
- Edit existing ones
- Remove messages
- View current list

### View Statistics

Monitor your contribution activity:
```bash
github-auto-commit
```
Select "📊 Stats" to see:
- Total commits
- Active days
- Average commits per day
- Recent activity

## 🛠️ Configuration

Configuration is stored in `~/.github_auto_commit/config.json`. You can:
- Backup configuration: Use "🔧 Setup" → "Backup config"
- Restore configuration: Use "🔧 Setup" → "Restore config"
- Reset to defaults: Use "🔧 Setup" → "Reset config"

## 🔒 Security

- Credentials are stored securely in your local configuration
- No data is sent to external servers
- All operations are performed locally
- Tokens are never exposed in commits

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with [Click](https://click.palletsprojects.com/)
- UI powered by [Rich](https://rich.readthedocs.io/)
- Interactive prompts by [Questionary](https://questionary.readthedocs.io/)
- Git operations via [GitPython](https://gitpython.readthedocs.io/)

## 📞 Support

If you encounter any issues or have questions:
1. Check the [Issues](https://github.com/vasanthfeb13/github-auto-commit/issues) page
2. Create a new issue if your problem isn't already listed
3. Provide as much detail as possible about your setup and the issue

---

Made with ❤️ by [Vasanth Adithya](https://github.com/vasanthfeb13)
