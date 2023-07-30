"""
The app setup.
"""

import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from sqlalchemy.orm import DeclarativeBase, MappedAsDataclass


class Base(DeclarativeBase, MappedAsDataclass):
    """SQLAlchemy Base model that is serailizeable"""
    pass


db = SQLAlchemy(model_class=Base)
loginManager = LoginManager()


def create_app(instance_path=None) -> Flask:
    """Application Factory for Flask"""
    app = Flask(__name__, instance_relative_config=True, instance_path=instance_path)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    app.config.from_pyfile("config.py")

    db.init_app(app)
    loginManager.init_app(app)

    with app.app_context():
        from . import auth

        app.register_blueprint(auth.auth)

        from . import tracker

        app.register_blueprint(tracker.tracker)
        app.add_url_rule("/", endpoint="index")

        from . import model

        db.create_all()

        model.populate_table()

        loginManager.login_view = "auth.login"  # type: ignore

    return app
