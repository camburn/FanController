""" Fan page for the fan controller project """

import json

import requests
from flask import Flask, render_template, request
from flask_assets import Bundle, Environment
from todo import todos

# Do not use localhost - werkzeug does weird things with ipv6
SERVER_NAME = "http://127.0.0.1:8000"

app = Flask(__name__)

assets = Environment(app)
css = Bundle("src/main.css", output="dist/main.css")
js = Bundle("src/*.js", output="dist/main.js")

assets.register("css", css)
assets.register("js", js)
css.build()
js.build()


@app.route("/cleo")
def cleo_page():
    """Fan Home Page"""
    return render_template("cleo.html")


@app.route("/")
def home_page():
    """Fan Home Page"""
    response = requests.get(
        f"{SERVER_NAME}/devices", headers={"accept": "application/json"}
    ).json()

    devices = [device["name"] for device in response]
    devices.insert(0, "Select Device")
    print(devices)
    return render_template("index.html", devices=devices)


@app.route("/commands")
def command_list():
    """Commands elements"""
    print("command Called")
    device_name = request.args.get("device")
    if not device_name or device_name == "Select Device":
        return render_template("commands.j2", commands=[])
    print("Get data")
    response = requests.get(
        f"{SERVER_NAME}/devices/{device_name}/capabilities",
        headers={"accept": "application/json"},
    ).json()
    print("returning response")
    return render_template("commands.j2", commands=response)


@app.route("/submit", methods=["POST"])
def submit_command():
    requests.post(
        f"{SERVER_NAME}/devices/{request.form["device"]}/commands",
        headers={"accept": "application/json"},
        json={"device_id": request.form["device"], "capability_id": request.form["command"]}
    )
    return json.dumps({"success": True}), 200, {"ContentType": "application/json"}


@app.route("/form")
def form_test():
    """Fan Home Page"""
    return render_template("form_page.html")


@app.route("/search", methods=["POST"])
def search_todo():
    search_term: str | None = request.form.get("search")

    if not search_term or len(search_term) == 0:
        return render_template("todo.html", todos=[])

    res_todos = []
    for todo in todos:
        if search_term in todo["title"]:
            res_todos.append(todo)

    return render_template("todo.html", todos=res_todos)


@app.route("/test", methods=["POST"])
def test_page():
    """Test page for testing htmx"""
    print(request.form)
    return "<p>Some information from python</p>"


if __name__ == "__main__":
    app.run(debug=True)
