from flask import Flask, request, render_template, make_response
from github_api import get_issue_information
from github import Issue
from typing import Optional

app = Flask(__name__, template_folder="../templates")


@app.route("/", methods=["GET"])
def base_route():
    res = render_template("index.html")
    response = make_response(res)
    response.headers["Content-Type"] = "text/html"
    return response


@app.route("/assignee", methods=["GET"])
def get_potential_assignee():
    issue_number = request.args.get('issue')  # number of the issue to get
    if not issue_number:
        return "error"  # TODO
    try:
        number: int = int(issue_number)
        issue_info: Optional[Issue] = get_issue_information(issue_number=number)
        if not issue_info:
            return "error3"  # TODO

        # TODO get list of potential assignee
        tmp = ["bob", "john", "smith"]
        res = render_template("assignee.html", title=issue_info.title, description=issue_info.body, number=number,
                              candidates=tmp)
        response = make_response(res)
        response.headers["Content-Type"] = "text/html"
        return response

    except Exception as err:
        print(err)
        return "error2"  # TODO



