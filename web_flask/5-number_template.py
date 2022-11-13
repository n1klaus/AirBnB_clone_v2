""" Module to start a Flask web application """
from flask import Flask, render_template, abort


app = Flask(__name__)


@app.route("/", strict_slashes=False)
def hello():
    """ Function to define route to '/' """
    return "Hello HBNB!"


@app.route("/hbnb", strict_slashes=False)
def hbnb():
    """ Function to define route to '/hbnb' """
    return "HBNB!"


@app.route("/c/<text>", strict_slashes=False)
def route_c(text):
    """ Function to define route to '/c' with variables as params """
    if text:
        text = text.replace("_", " ")
        return "C " + text


@app.route("/python/", strict_slashes=False)
@app.route("/python/<text>", strict_slashes=False)
def route_python(text="is cool"):
    """ Function to define route to '/python'
        with optional variables as params
    """
    if text:
        text = text.replace("_", " ")
    return "Python " + text


@app.route("/number/<n>", strict_slashes=False)
def route_number(n):
    """ Function to define route to '/number' with variables as params
    """
    try:
        if n.isnumeric():
            return n + " is a number"
        raise
    except BaseException:
        abort(404)


@app.route("/number_template/<n>", strict_slashes=False)
def route_number_template(n):
    """ Function to define route to '/number_template' with variables as params
        and render html page if variable is a number
    """
    try:
        if n.isnumeric():
            return render_template("5-number.html", number=n)
        raise
    except BaseException:
        abort(404)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
