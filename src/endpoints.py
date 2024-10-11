from flask import Flask


app = Flask(__name__, template_folder="../templates")


@app.route("/", methods=["GET"])
def base_route():
    return "TODO"



