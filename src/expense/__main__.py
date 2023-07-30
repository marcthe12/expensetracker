import click
from flask.cli import FlaskGroup
from . import create_app


@click.group(cls=FlaskGroup, create_app=create_app)
def cli() -> None:
    """The Main CLI so we can run it without using flask"""
    pass


if __name__ == "__main__":
    cli()
