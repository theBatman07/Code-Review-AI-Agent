from github import Github
from typing import List, Dict
import base64

class GitHubService:
    def __init__(self, token: str = None):
        self.github = Github(token)

    def get_pr_files(self, repo_url: str, pr_number: int) -> List[Dict]:
        repo_name = repo_url.split('github.com/')[-1]
        repo = self.github.get_repo(repo_name)
        pr = repo.get_pull(pr_number)
        
        files = []
        for file in pr.get_files():
            if file.status != "removed":
                content = base64.b64decode(
                    repo.get_contents(file.filename, ref=pr.head.sha).content
                ).decode()
                files.append({
                    "name": file.filename,
                    "content": content,
                    "patch": file.patch
                })
        return files