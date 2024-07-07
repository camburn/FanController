""" Fan page for the fan controller project """

from flask import Flask, render_template, request
from flask_assets import Bundle, Environment
from todo import todos

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
    return render_template("index.html")


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
