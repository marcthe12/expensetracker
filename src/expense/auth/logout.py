from flask import redirect, url_for
from flask_login import login_required, logout_user
from werkzeug import Response

from .blueprint import auth

@auth.route("/logout")
@login_required
def logout() -> Response:
    """
    Logout user View.
    """
    logout_user()
    return redirect(url_for("index"))
