from github import Github, Repository, PaginatedList, NamedUser, Issue, Event
from github import Auth
from dotenv import load_dotenv
import os
from typing import Optional

load_dotenv()
API_KEY: str = os.getenv("API_KEY")

auth = Auth.Token(API_KEY)
github_instance: Github = Github(auth=auth, per_page=100)


def get_issue_information(issue_number: int) -> Optional[Issue]:
    try:
        repo: Repository = github_instance.get_repo("microsoft/vscode")  # can this line be avoided???
        res_issue: Issue = repo.get_issue(number=issue_number)
        if not res_issue:
            return None
        return res_issue
    except Exception as err:
        print(err)
        return None


def get_user_events(user_name: str):
    repo: Repository = github_instance.get_repo("microsoft/vscode")
    commits: PaginatedList = repo.get_commits(author=user_name)
    print(commits.totalCount)
    pass


if __name__ == '__main__':
    get_user_events(user_name="hediet")
    pass
