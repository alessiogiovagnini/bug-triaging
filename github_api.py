import sys
from pathlib import Path

from github import Github, Repository, PaginatedList, NamedUser
from github import Auth
from dotenv import load_dotenv
from typing import Optional
import os
from string_cleaning import clean_string
import csv

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

    csv_header: list[str] = ["number", "title", "assignee", "body"]
    csv_rows: list[list] = [csv_header]

    i: int = 0
    not_finished: bool = True
    while not_finished:
        current_issues: list = issues.get_page(i)
        print(f"Current page: {i}")
        if len(current_issues) == 0:  # the list is empty if the page do not exist
            not_finished = False
            break
        else:
            for issue in current_issues:
                assignees: list[NamedUser] = issue.assignees  # list of assignee
                number: int = issue.number
                title: str = issue.title
                body: str = issue.body or ""

                # print(f"current number: {number}")
                #  training set will be composed by all vscode’s issues that (i) are closed; (ii) have exactly
                #  one assignee; and (iii) have an issue id ≤ 210000. The test set are from number 210001 to 220000.

                if len(assignees) == 1 and number <= 220000:
                    assignee: NamedUser = assignees[0]
                    assignee_login: str = assignee.login

                    cleaned_body: str = clean_string(text=body)

                    csv_rows.append([number, title, assignee_login, cleaned_body])

                if number > 220000:
                    not_finished = False
                    break
        i = i + 1

    output_file_name: Path = Path("output.csv")

    file = open(output_file_name, "w")

    with file:
        writer = csv.writer(file)
        writer.writerows(csv_rows)

    file.close()

    print(f"Script end")
    sys.exit(0)





