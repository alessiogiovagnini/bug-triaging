# bug-triaging
Project 1 for Software Analytics on bug triaging

# Other info
1. If possible use type annotations `a: str = get_name()`
2. Make new branches for features/fixes
3. Before a pull request get the branch up to date with the main one
4. Have at least one other team member approve the pull request (unless is a small fix)
5. IDK, add here other stuff if needed

# Useful git commands
### Get latest changes
`git pull`
### Add file to commit
`git add <file>` to add all files `git add .`
### To commit changes
`git commit -m "<message of commit>"`
### To push
`git push`
### Switch branch
`git switch <branch name>`
### Create new branch
`git switch -c <new branch name>`
### In case the branch is behind main 
this will merge main into the current branch:
`git merge main`, if there are conflict I suggest to use an ide to solve them

# Installing
creating virtual env
```shell
 python3.12 -m venv .venv
```
activating it
```shell
source .venv/bin/activate
```
check if is correct
```shell
which python
```
installing requirements
```shell
pip install -r requirement.txt
```

# Add local Api key
Create a file named `.env ` and add the github key, use the file
`example.env` as a guide. 
### !!! Do not push any file containing secret keys !!!