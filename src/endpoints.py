from pathlib import Path
from flask import request, render_template, make_response, Flask
import flask
from src.github_calls import get_issue_information
from github import Issue
from typing import Optional
from src.prediction import predict_assignee
from transformers import AutoModelForSequenceClassification, AutoTokenizer
import json
import torch

app = Flask(__name__, template_folder="../templates")


model_path: Path = Path("./results/checkpoint-14102024")
model_name: str = "distilbert-base-uncased"
model = AutoModelForSequenceClassification.from_pretrained(model_path.as_posix())
tokenizer = AutoTokenizer.from_pretrained(model_name)

device = torch.device('cpu')

model.to(device)

label_path: Path = Path("./labels_json.json")
with open(label_path) as f:
    labels = json.load(f)


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

        predictions: list = predict_assignee(title=issue_info.title, body=issue_info.body,
                                            tokenizer=tokenizer, device=device, model=model, labels=labels)

        res = render_template("assignee.html", title=issue_info.title, description=issue_info.body, number=number,
                              candidates=predictions)
        response = make_response(res)
        response.headers["Content-Type"] = "text/html"
        return response

    except Exception as err:
        print(err)
        return flask.redirect("/500")



