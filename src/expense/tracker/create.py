from datetime import date
from flask import (
    redirect,
    render_template,
    url_for,
)
from flask_login import login_required, current_user

from .. import db

from flask_wtf import FlaskForm
from wtforms import (
    DateField,
    TextAreaField,
    DecimalField,
    SubmitField,
    SelectField,
)
from wtforms.widgets import NumberInput
from wtforms.validators import InputRequired

from ..model import Category, Expense
from .blueprint import tracker


class CreateForm(FlaskForm):
    """
    The Form to create a entry
    """
    description = TextAreaField()
    date = DateField(
        validators=[InputRequired()], format="%Y-%m-%d", default=date.today
    )
    amount = DecimalField(places=2, validators=[InputRequired()], widget=NumberInput(), default=0)  # type: ignore
    category = SelectField(coerce=int)  # type: ignore
    submit = SubmitField()

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.category.choices = [(cat.id, cat.name) for cat in current_user.categories]  # type: ignore


@tracker.route("/create", methods=["GET", "POST"])
@login_required
def create():
    """The view to handle new entry"""
    form = CreateForm()
    if form.validate_on_submit():
        cat = db.session.scalars(
            db.select(Category).where(Category.id == form.category.data)
        ).one()
        expense = Expense(
            description=form.description.data,
            date=form.date.data,
            amount=form.amount.data,
            category=cat,
        )  # type: ignore
        current_user.expenses.append(expense)  # type: ignore
        db.session.commit()
        return redirect(url_for("index"))
    return render_template("tracker/create.html", form=form)
