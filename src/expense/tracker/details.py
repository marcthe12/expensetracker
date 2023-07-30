from flask import (
    render_template,
)
from flask_login import current_user, login_required
from sqlalchemy import func
from .blueprint import tracker
from ..model import Expense
from .. import db


@tracker.route("/details")
@login_required
def details() -> str:
    """
    The detail table of all the expenses
    """
    total = db.session.scalars(
        db.select(func.coalesce(func.sum(Expense.amount), 0)).where(
            Expense.user == current_user
        )
    ).all()
    return render_template("tracker/details.html", total=total)
