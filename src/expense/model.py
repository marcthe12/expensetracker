from typing import List
import datetime

from flask_login import UserMixin
from sqlalchemy import Column, Float, Integer, String, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .auth.password import PasswordHash, Password
from . import db

user_category = db.Table(
    "user_category_map",
    Column("user_id", Integer, ForeignKey("user.id"), primary_key=True),
    Column("category_id", Integer, ForeignKey("category.id"), primary_key=True),
)

class User(db.Model, UserMixin):
    """The table for Username and Password"""
    id: Mapped[int] = mapped_column(primary_key=True, init=False)
    name: Mapped[str] = mapped_column(String(64), unique=True, comment="The username")
    password: Mapped[PasswordHash] = mapped_column(Password(), comment="The password as a hash")
    expenses: Mapped[List["Expense"]] = relationship(
        back_populates="user",
        order_by="Expense.date",
        cascade="all, delete",
        init=False,
    )
    categories: Mapped[List["Category"]] = relationship(
        secondary=user_category, init=False
    )


class Category(db.Model):
    """The List of categories, contains both user defined and predefined"""
    id: Mapped[int] = mapped_column(primary_key=True, init=False)
    name: Mapped[str] = mapped_column(String(256), nullable=False, unique=True)


class Expense(db.Model):
    """The list of expenses"""
    id: Mapped[int] = mapped_column(primary_key=True, init=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), init=False)
    user = relationship(User, back_populates="expenses")
    date: Mapped[datetime.date] = mapped_column()
    amount: Mapped[float] = mapped_column(Float(2))
    category_id: Mapped[int] = mapped_column(ForeignKey("category.id"), init=False)
    category: Mapped[Category] = relationship(cascade="all, delete")
    description: Mapped[str] = mapped_column(Text(), default="")


def populate_table() -> None:
    """
    Create the initial entries for the table.
    Currently populates the Category table with predefined values
    """
    for cat in ["Misc", "Income"]:
        if db.session.scalars(
            db.select(Category).where(Category.name == cat)
        ).one_or_none():
            continue
        db.session.add(Category(name=cat)) # type: ignore

    db.session.commit()
