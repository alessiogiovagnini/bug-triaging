# bug-triaging
Project 1 for Software Analytics on bug triaging

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

# running the server
Before running a trained model must be provided, the path can be added in the .env
file. Follow the example in `example.rnv`.
Then to run the server simply run the `main.py`
```shell
python3 main.py
```
The server will start on localhost 3000, the front-end is composed by one
search page where it is possible to insert an issue number and a list of
the best five candidate will be displayed.


# Using the scripts
All the scripts are located under the folder `scripts`

### Github API
This script produce the csv with all the issue collected from the 
VsCode repository. 
Simply run: `python3 github_api.py`

### Cleaning tool
This script is used to apply the cleaning on the csv.
Use: ` python3 cleaning_tool.py --help` to list the usage

### Training
The scripts `training.py` and `trainingOnNewestissues.py` are used to
produce the models.

### Others scripts
The other scripts were used to test some processes


# Project structure
Under the folder `src` are all the file to run the server and helper functions.
In `templates` are the html pages. In `labels` are stored the names of the
assignee that can be returned by the app.