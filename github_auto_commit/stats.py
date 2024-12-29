"""Statistics module for GitHub Auto Commit."""
import os
from datetime import datetime, timedelta
from collections import defaultdict
import requests
from rich.console import Console
from rich.table import Table
from rich.progress import Progress
from rich import box

console = Console()

class ContributionStats:
    """Class to handle contribution statistics."""
    
    def __init__(self, token):
        """Initialize with GitHub token."""
        self.token = token
        self.headers = {
            'Authorization': f'token {token}',
            'Accept': 'application/vnd.github.v3+json'
        }
        
    def get_user_stats(self, username, days=30):
        """Get user contribution statistics."""
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        # Get user's repositories
        repos_url = f'https://api.github.com/users/{username}/repos'
        response = requests.get(repos_url, headers=self.headers)
        repos = response.json()
        
        stats = defaultdict(int)
        repo_stats = defaultdict(int)
        
        with Progress() as progress:
            task = progress.add_task("[cyan]Analyzing repositories...", total=len(repos))
            
            for repo in repos:
                repo_name = repo['name']
                commits_url = f'https://api.github.com/repos/{username}/{repo_name}/commits'
                params = {'since': start_date.isoformat(), 'author': username}
                
                try:
                    response = requests.get(commits_url, headers=self.headers, params=params)
                    commits = response.json()
                    
                    if isinstance(commits, list):
                        for commit in commits:
                            date = commit['commit']['author']['date'][:10]
                            stats[date] += 1
                            repo_stats[repo_name] += 1
                            
                except Exception as e:
                    console.print(f"[yellow]Warning: Could not fetch commits for {repo_name}: {str(e)}[/yellow]")
                
                progress.update(task, advance=1)
        
        return stats, repo_stats
    
    def display_stats(self, username, days=30):
        """Display contribution statistics in a rich table."""
        stats, repo_stats = self.get_user_stats(username, days)
        
        # Summary table
        summary = Table(title="📊 Contribution Summary", box=box.ROUNDED)
        summary.add_column("Metric", style="cyan")
        summary.add_column("Value", style="green")
        
        total_commits = sum(stats.values())
        active_days = len(stats)
        avg_commits = total_commits / days if days > 0 else 0
        
        summary.add_row("Total Commits", str(total_commits))
        summary.add_row("Active Days", str(active_days))
        summary.add_row("Average Commits/Day", f"{avg_commits:.2f}")
        summary.add_row("Most Active Day", max(stats.items(), key=lambda x: x[1])[0] if stats else "N/A")
        
        console.print(summary)
        console.print()
        
        # Repository breakdown
        if repo_stats:
            repo_table = Table(title="📚 Repository Breakdown", box=box.ROUNDED)
            repo_table.add_column("Repository", style="cyan")
            repo_table.add_column("Commits", style="green")
            repo_table.add_column("Percentage", style="yellow")
            
            for repo, commits in sorted(repo_stats.items(), key=lambda x: x[1], reverse=True):
                percentage = (commits / total_commits * 100) if total_commits > 0 else 0
                repo_table.add_row(repo, str(commits), f"{percentage:.1f}%")
            
            console.print(repo_table)
            console.print()
        
        # Activity heatmap
        console.print("🔥 Activity Heatmap")
        self._display_heatmap(stats, days)
    
    def _display_heatmap(self, stats, days):
        """Display an ASCII heatmap of contributions."""
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        current_date = start_date
        calendar = []
        week = []
        
        # Fill in missing dates with zero commits
        while current_date <= end_date:
            date_str = current_date.strftime('%Y-%m-%d')
            count = stats.get(date_str, 0)
            
            # Determine color based on commit count
            if count == 0:
                color = "white"
            elif count <= 2:
                color = "green"
            elif count <= 5:
                color = "yellow"
            else:
                color = "red"
            
            week.append((date_str, count, color))
            
            if current_date.weekday() == 6:
                calendar.append(week)
                week = []
            
            current_date += timedelta(days=1)
        
        if week:
            calendar.append(week)
        
        # Print weekday headers
        console.print("   Mo Tu We Th Fr Sa Su")
        
        # Print calendar with colored squares
        for week in calendar:
            line = ""
            for date, count, color in week:
                if count == 0:
                    symbol = "⬜"
                elif count <= 2:
                    symbol = "🟩"
                elif count <= 5:
                    symbol = "🟨"
                else:
                    symbol = "🟥"
                line += f" {symbol}"
            console.print(line)
        
        # Print legend
        console.print("\nLegend:")
        console.print("⬜ No commits  🟩 1-2 commits  🟨 3-5 commits  🟥 >5 commits")
