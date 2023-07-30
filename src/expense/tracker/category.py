from typing import Union
from flask import (
    redirect,
    render_template,
    url_for,
)
from flask_login import login_required, current_user
from werkzeug import Response

from .. import db

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import InputRequired

from ..model import Category
from .blueprint import tracker


class CategoryForm(FlaskForm):
    """Add Category"""
    category = StringField("Add Category", validators=[InputRequired()])  # type: ignore
    submit = SubmitField()


@tracker.route("/category", methods=["GET", "POST"])
@login_required
def category() -> Union[str, Response]:
    """
    To manage the list of user defined capabilities
    """
    form = CategoryForm()
    if form.validate_on_submit():
        category = form.category.data
        cat = db.session.scalars(
            db.select(Category).where(Category.name == category)
        ).one_or_none()
        if cat is None:
            cat = Category(name=category)
        current_user.categories.append(cat)  # type: ignore
        db.session.commit()
        return redirect(url_for("index"))
    return render_template("tracker/category.html", form=form)
