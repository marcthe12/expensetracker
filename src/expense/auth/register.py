"""Register User"""
from typing import Union
from flask import (
    redirect,
    render_template,
    url_for,
)
from flask_login import current_user, login_user

from flask_wtf import FlaskForm
from werkzeug import Response
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import (
    DataRequired,
    InputRequired,
    Length,
    ValidationError,
    EqualTo,
)

from ..model import User, Category

from .password import PasswordHash

from .blueprint import auth
from .. import db


class RegisterForm(FlaskForm):
    """User Registeration form"""
    username = StringField(validators=[DataRequired(), InputRequired(), Length(max=64)])
    password = PasswordField(
        validators=[
            DataRequired(),
            InputRequired(),
            Length(min=8, message="Select a stronger password."),
        ]
    )
    confirm = PasswordField(
        "Repeat Password",
        validators=[
            DataRequired(),
            InputRequired(),
            EqualTo("password", message="Passwords must match."),
        ],
    )
    submit = SubmitField("Register")

    def validate_username(self, field: StringField) -> None:
        user = db.session.execute(
            db.select(User).where(User.name == field.data)
        ).first()
        if user is not None:
            raise ValidationError("Please use a different username.")


@auth.route("/register", methods=("GET", "POST"))
def register() -> Union[str, Response]:
    """
    Registering User Route
    Support both POST and GET
    """
    if current_user.is_authenticated:  # type: ignore
        return redirect(url_for("index"))
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(name=form.username.data, password=PasswordHash.new(form.password.data))  # type: ignore

        for cat in ["Misc", "Income"]:
            category = db.session.scalars(
                db.select(Category).where(Category.name == cat)
            ).one()
            user.categories.append(category)

        db.session.add(user)
        db.session.commit()
        login_user(user)
        return redirect(url_for("index"))
    return render_template("auth/register.html", form=form)
