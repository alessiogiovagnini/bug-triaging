import sys
from github import Github, Repository, PaginatedList, NamedUser
from github import Auth
from dotenv import load_dotenv
from typing import Optional
import os

load_dotenv()
API_KEY: str = os.getenv("API_KEY")

if __name__ == '__main__':
    auth = Auth.Token(API_KEY)

    github_instance: Github = Github(auth=auth, per_page=100)

    # tuple, first number is request remaining, second is max allowed
    rate_limit: tuple[int, int] = github_instance.rate_limiting
    reset_time: int = github_instance.rate_limiting_resettime  # reset time of request allowed
    print(f"Rate limit: {rate_limit[0]}")
    repository: Repository = github_instance.get_repo("microsoft/vscode")

    # only accept closed, the # order is to start from 1
    issues: PaginatedList = repository.get_issues(state="closed", direction="asc")
    print(f"Total number of issues found: {issues.totalCount}")

    i: int = 0
    while True:
        current_issues: list = issues.get_page(i)
        pass
        if len(current_issues) == 0:
            break
        else:
            for issue in current_issues:
                assignees: list[NamedUser] = issue.assignees  # list of assignee
                number: int = issue.number
                title: str = issue.title
                body: Optional[str] = issue.body
                #
                # #  training set will be composed by all vscode’s issues that (i) are closed; (ii) have exactly
                # #  one assignee; and (iii) have an issue id ≤ 210000
                #
                # # TODO test set 210001 to 220000.
                # if len(assignees) == 1 and number <= 210000:
                #     assignee: NamedUser = assignees[0]
                #     # print(f"saved issue --> num: {number}")
                #     # TODO store all the issues, maybe already clean the text
                #     print(f"URL ---> {issue.url}")
                # else:
                #     print(f"Discarded issue --> assignees num: {len(assignees)}, num: {number}")
                #     pass
                # if number > 220000:
                #     break
                pass
        i = i + 1

    print(f"Script end")
    sys.exit(0)





