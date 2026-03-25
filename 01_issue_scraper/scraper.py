import requests
import os
from datetime import datetime, timedelta

# Configuration
REPO_FILE = 'idea_01_issue_scraper/repos.txt'
RESULTS_FILE = 'idea_01_issue_scraper/results.txt'
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN') # Provided by GH Actions

def get_new_issues(repo):
    # Calculate timestamp for 24 hours ago
    yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%dT%H:%M:%SZ')
    url = f"https://api.github.com/repos/{repo}/issues"
    params = {
        'labels': 'good first issue',
        'since': yesterday,
        'state': 'open'
    }
    headers = {'Authorization': f'token {GITHUB_TOKEN}'} if GITHUB_TOKEN else {}
    
    response = requests.get(url, params=params, headers=headers)
    if response.status_code == 200:
        return response.json()
    return []

def main():
    with open(REPO_FILE, 'r') as f:
        repos = [line.strip() for line in f if line.strip()]

    new_entries = []
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    for repo in repos:
        issues = get_new_issues(repo)
        for issue in issues:
            # Avoid pull requests (GH API treats PRs as issues)
            if 'pull_request' not in issue:
                entry = f"[{timestamp}] {repo} | {issue['title']} | {issue['html_url']}\n"
                new_entries.append(entry)

    if new_entries:
        with open(RESULTS_FILE, 'a') as f:
            f.writelines(new_entries)
        print(f"Added {len(new_entries)} new issues.")
    else:
        print("No new issues found today.")

if __name__ == "__main__":
    main()