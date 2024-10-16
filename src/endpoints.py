from flask import request, render_template, make_response
import flask
from github_api import get_issue_information
from github import Issue
from typing import Optional
from prediction import predict_assignee
from main import app

@app.route("/", methods=["GET"])
def base_route():
    res = render_template("index.html")
    response = make_response(res)
    response.headers["Content-Type"] = "text/html"
    return response


@app.errorhandler(404)
def page_not_found(e):
    print(e)
    res = render_template("error.html")
    response = make_response(res)
    response.headers["Content-Type"] = "text/html"
    return response


@app.errorhandler(400)
def bad_request(e):
    return f"Bad request: {e}"


@app.errorhandler(500)
def internal_error(e):
    return f"Internal server error: {e}"


@app.route("/assignee", methods=["GET"])
def get_potential_assignee():
    issue_number = request.args.get('issue')  # number of the issue to get
    if not issue_number:
        return flask.redirect("/400")
    try:
        number: int = int(issue_number)
        issue_info: Optional[Issue] = get_issue_information(issue_number=number)
        if not issue_info:
            return flask.redirect("/404")

        # TODO test if it works
        prediction: list = predict_assignee(title=issue_info.title, body=issue_info.body)
        res = render_template("assignee.html", title=issue_info.title, description=issue_info.body, number=number,
                              candidates=prediction)
        response = make_response(res)
        response.headers["Content-Type"] = "text/html"
        return response

    except Exception as err:
        print(err)
        return flask.redirect("/500")



