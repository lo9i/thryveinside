from flask import render_template

from . import landing


@landing.route("/")
def index():
    return render_template('index.html')
