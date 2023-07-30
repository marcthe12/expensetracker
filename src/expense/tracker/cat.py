from flask import (
    render_template,
)
from flask_login import current_user, login_required
from sqlalchemy import func
from .blueprint import tracker
from ..model import Category, Expense
from .. import db


@tracker.route("/cat/<int:id>")
@login_required
def cat(id: int) -> str:
    """
    The per category view of the the user expense.
    """
    category = db.one_or_404(db.select(Category).where(Category.id == id))

    total = db.session.scalars(
        db.select(func.coalesce(func.sum(Expense.amount), 0)).where(
            Expense.user == current_user, Expense.category == category
        )
    ).all()
    table = db.session.scalars(
        db.select(Expense).where(
            Expense.user == current_user, Expense.category == category
        )
    ).all()
    return render_template("tracker/cat.html", table=table, total=total, category=category)
