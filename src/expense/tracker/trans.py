from typing import Union
from flask import (
    redirect,
    render_template,
    url_for,
)
from flask_login import login_required, current_user
from werkzeug import Response

from .. import db
from ..model import Category, Expense
from .blueprint import tracker
from .create import CreateForm

from wtforms import SubmitField


class TransForm(CreateForm):
    """
    Editing the transaction.
    Adds the delete button
    """
    delete = SubmitField()


@tracker.route("/trans/<int:id>", methods=["GET", "POST"])
@login_required
def trans(id: int) -> Union[str, Response]:
    """
    Edits the transaction. It also has the capability of deleting it.
    """
    expense: Expense = db.one_or_404(db.select(Expense).where(Expense.id == id, Expense.user == current_user))  # type: ignore
    form: TransForm = TransForm(
        description=expense.description,
        date=expense.date,
        amount=expense.amount,
        category_id=expense.category.id,
    )
    form.category.choices = [(cat.id, cat.name) for cat in current_user.categories]  # type: ignore
    if form.validate_on_submit():
        if form.delete.data:
            db.session.delete(expense)
        elif form.submit.data:
            cat = db.session.scalars(
                db.select(Category).where(Category.id == form.category.data)
            ).one()
            expense.description = form.description.data
            expense.date = form.date.data  # type: ignore
            expense.amount = form.amount.data  # type: ignore
            expense.category = cat

            current_user.expenses.append(expense)  # type: ignore

        db.session.commit()
        return redirect(url_for("index"))
    return render_template("tracker/trans.html", form=form)
