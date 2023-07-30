from typing import Optional, Union
from flask import (
    redirect,
    render_template,
    request,
    url_for,
)
from flask_login import current_user, login_user

from flask_wtf import FlaskForm
from werkzeug import Response
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, InputRequired

from .blueprint import auth
from ..model import User
from .. import db


class LoginForm(FlaskForm):
    """
    The Login Form.
    The validate method has be improved to do validating the user
    """
    username = StringField(validators=[DataRequired(), InputRequired()])
    password = PasswordField(validators=[DataRequired(), InputRequired()])
    submit = SubmitField("Log In")

    def validate(self, *args, **kwargs):
        if not super().validate(*args, **kwargs):
            return False

        username = self.username.data
        password = self.password.data

        user = db.session.scalars(
            db.select(User).where(User.name == username)
        ).one_or_none()
        if user is None:
            self.username.errors.append("Invalid username")  # type: ignore
            return False

        if not user.password == password:
            self.password.errors.append("Invalid password")  # type: ignore
            return False

        self.user = user
        return True


@auth.route("/login", methods=("GET", "POST"))
def login() -> Union[str, Response]:
    """
    The view for Loging in the User
    """
    if current_user.is_authenticated:  # type: ignore
        return redirect(request.args.get("next", default=url_for("index")))
    form = LoginForm()
    if form.validate_on_submit():
        login_user(form.user)
        return redirect(request.args.get("next", default=url_for("index")))

    return render_template("auth/login.html", form=form)
