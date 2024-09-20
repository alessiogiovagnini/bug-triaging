from github import Github, Repository, PaginatedList, NamedUser
from github import Auth
from dotenv import load_dotenv
from typing import Optional
import os

load_dotenv()
API_KEY: str = os.getenv("API_KEY")

if __name__ == '__main__':
    auth = Auth.Token(API_KEY)

    github_instance: Github = Github(auth=auth)

    # tuple, first number is request remaining, second is max allowed
    rate_limit: tuple[int, int] = github_instance.rate_limiting
    reset_time: int = github_instance.rate_limiting_resettime  # reset time of request allowed

    repository: Repository = github_instance.get_repo("microsoft/vscode")

    issues: PaginatedList = repository.get_issues(state="closed")

    for issue in issues:
        assignees: list[NamedUser] = issue.assignees  # list of assignee
        number: int = issue.number
        title: str = issue.title
        body: Optional[str]

        raw = issue.raw_data  # just in case
        # TODO filter and store all the issues
    pass





