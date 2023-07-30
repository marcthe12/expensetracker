from typing import Union
from flask import redirect, url_for, render_template
from flask_login import current_user, login_required, logout_user
from flask_wtf import FlaskForm
from werkzeug import Response
from wtforms import SubmitField

from ..model import User
from .blueprint import auth, db


class DeleteForm(FlaskForm):
    """To Handle Delete the user"""
    submit = SubmitField("Delete")


@auth.route("/delete", methods=["GET", "POST"])
@login_required
def delete() -> Union[str, Response]:
    """
    Delete the user account. Has both GET and POST
    """
    form = DeleteForm()
    if form.validate_on_submit():
        user_id = current_user.id  # type: ignore
        logout_user()
        user = db.session.scalars(db.select(User).where(User.id == user_id)).one()
        db.session.delete(user)
        db.session.commit()
        return redirect(url_for("index"))
    return render_template("auth/delete.html", form=form)
