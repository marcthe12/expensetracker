from flask import render_template, jsonify
from werkzeug import Response
from werkzeug.local import LocalProxy
from flask_login import current_user, login_required
from .blueprint import tracker


@tracker.route("/")
@login_required
def index() -> str:
    """
    The dashboard
    """
    return render_template("tracker/index.html")


@tracker.route("/summary.json")
@login_required
def summary() -> Response:
    """
    The Summary Api
    Returns the list of all of the user expenses in json
    """
    return jsonify(current_user.expenses)  # type: ignore
