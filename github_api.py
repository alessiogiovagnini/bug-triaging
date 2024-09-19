from github import Github
from github import Auth
from dotenv import load_dotenv
import os

load_dotenv()
API_KEY: str = os.getenv("API_KEY")

if __name__ == '__main__':
    auth = Auth.Token(API_KEY)

    github_instance: Github = Github(auth=auth)

    for repo in github_instance.get_user().get_repos():
        print(repo.name)

