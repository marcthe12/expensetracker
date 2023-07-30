from flask import Blueprint

tracker = Blueprint("tracker", __name__)

from . import create, index, trans, category, cat, details
