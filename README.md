# GitHub Auto Commit 🚀

A powerful command-line tool for automating GitHub contributions with customizable schedules and patterns.

## Features ✨

- 🕒 **Flexible Scheduling**: Set custom hours and days for commits
- 📊 **Customizable Patterns**: Choose from preset commit patterns or create your own
- 🔄 **Quick Commits**: Make immediate contributions without waiting for schedule
- 🔐 **Secure**: Uses GitHub Personal Access Token for authentication
- 📱 **User-Friendly**: Interactive CLI with clear feedback and status updates

## Installation 📦

```bash
pip install github-auto-commit
```

## Quick Start 🚀

1. **Setup your GitHub credentials**:
```bash
github-auto-commit setup --username YOUR_USERNAME --token YOUR_TOKEN
```

2. **Configure your commit schedule**:
```bash
github-auto-commit configure
```

3. **Start making contributions**:
```bash
# Start scheduled service
github-auto-commit start

# Or make quick commits
github-auto-commit quick-commit --count 3
```

## Available Commands 🛠️

- `setup`: Configure GitHub credentials
- `configure`: Interactive configuration wizard
- `start`: Start the auto-commit service
- `quick-commit`: Make immediate commits
- `set-schedule`: Customize commit schedule
- `set-frequency`: Set commit frequency
- `status`: View current configuration
- `help`: Show detailed help

## Schedule Presets 📅

- **Work Hours**: 9 AM - 5 PM, weekdays
- **Evening Only**: 6 PM - 10 PM, weekdays
- **Weekend Warrior**: 10 AM - 8 PM, weekends
- **Night Owl**: 8 PM - 2 AM, weekdays

## Commit Patterns 📊

- **Light**: 1-2 commits per day
- **Moderate**: 2-4 commits per day
- **Heavy**: 4-8 commits per day
- **Custom**: Set your own range

## Configuration Example 🔧

```bash
# Set evening schedule
github-auto-commit set-schedule --start-hour 18 --end-hour 22 --days "monday,wednesday,friday"

# Set custom commit frequency
github-auto-commit set-frequency --pattern custom --min-commits 3 --max-commits 5
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
