""" Module to start a Flask web application """
from flask import Flask


app = Flask(__name__)


@app.route("/", strict_slashes=False)
def hello():
    """ Function to define route to '/' """
    return f"Hello HBNB!"


@app.route("/hbnb", strict_slashes=False)
def hbnb():
    """ Function to define route to '/hbnb' """
    return f"HBNB!"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
