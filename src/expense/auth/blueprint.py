from typing import Optional
from flask import Blueprint

from ..model import User
from .. import loginManager, db

auth = Blueprint("auth", __name__, url_prefix="/auth")


@loginManager.user_loader
def load_user(id: str) -> Optional[User]:
    """
    Callback to load user from id which is a number
    """
    if id is not None:
        return db.session.scalars(db.select(User).where(User.id == id)).one_or_none()
    return None


from . import login, logout, register, delete
