import sys
from pathlib import Path
import time
from github import Github, Repository, PaginatedList, NamedUser, Issue
from github import Auth
from dotenv import load_dotenv
import os
from src.string_cleaning import clean_string, clean_markdown_string
import csv
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


if __name__ == '__main__':
    start: float = time.time()

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

    try:
        i: int = 0
        not_finished: bool = True
        while not_finished:
            # check if we still have requests
            if github_instance.rate_limiting[0] < 10:
                print(f"request limit hit, waiting for {reset_time - time.time()} seconds")
                time.sleep(reset_time - time.time() + 10)
            current_issues: list = issues.get_page(i)
            print(f"Current page: {i}")
            if len(current_issues) == 0:  # the list is empty if the page do not exist
                not_finished = False
                break
            else:
                for issue in current_issues:
                    assignees: list[NamedUser] = issue.assignees  # list of assignee
                    number: int = issue.number
                    title: str = clean_string(text=issue.title)
                    body: str = issue.body or ""
                    html_url: str = issue.html_url  # issues and pull request are mixed together, this is to filter pull
                    split_url: list[str] = html_url.split("/")
                    is_issue: str = split_url[5]

                    #  training set will be composed by all vscode’s issues that (i) are closed; (ii) have exactly
                    #  one assignee; and (iii) have an issue id ≤ 210000. The test set are from number 210001 to 220000.

                    if len(assignees) == 1 and number <= 220000 and is_issue == "issues":
                        assignee: NamedUser = assignees[0]
                        assignee_login: str = assignee.login

                        cleaned_body: str = clean_markdown_string(text=body)

                        csv_rows.append([number, title, assignee_login, cleaned_body])

            i = i + 1
    except Exception as e:
        output_file_name: Path = Path("partial_output.csv")

        file = open(output_file_name, "w")

        with file:
            writer = csv.writer(file)
            writer.writerows(csv_rows)

        file.close()

        print(f"Script end with error:")
        print(e)
        sys.exit(1)

    output_file_name: Path = Path("output.csv")

    file = open(output_file_name, "w")

    with file:
        writer = csv.writer(file)
        writer.writerows(csv_rows)

    file.close()

    end: float = time.time()
    print(f"Script ended in {(end - start) / 60} minutes")
    sys.exit(0)





