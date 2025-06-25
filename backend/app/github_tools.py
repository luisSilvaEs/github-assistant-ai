import os
import requests

GITHUB_PAT = os.getenv("GITHUB_PAT")
GITHUB_USER = os.getenv("GITHUB_USER")

def get_last_commits(repo_name: str, count: int = 3):
    headers = {"Authorization": f"token {GITHUB_PAT}"}
    url = f"https://api.github.com/repos/{GITHUB_USER}/{repo_name}/commits"
    response = requests.get(url, headers=headers, params={"per_page": count})
    response.raise_for_status()
    data = response.json()
    return [
        {
            "date": c["commit"]["committer"]["date"],
            "sha": c["sha"][:7],
            "message": c["commit"]["message"]
        }
        for c in data
    ]
