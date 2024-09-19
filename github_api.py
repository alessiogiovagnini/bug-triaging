from github import Github
from dotenv import load_dotenv
import os

load_dotenv()
API_KEY: str = os.getenv("API_KEY")

if __name__ == '__main__':
    print(API_KEY)

