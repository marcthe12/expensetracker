# Expense Tracker

This is app to manage your finances by the manages your expenses. It also allows users to define their own categories.

## Installation

The program is written using flask targeting python 3.11.4
To build this program, use the following steps

```bash
pip install .
```

It is recommended to use a virtual environment to install the program.

```bash
python -m venv venv
#POSIX shell(For Linux and Mac)
. venv/bin/activate
```

You also need the relevant database drivers installed which can be obtained from pip.
For production, use a WGSI server(like gunicorn)

## Configuration

In the instance directory (refer to [docs](https://flask.palletsprojects.com/en/2.3.x/config/#instance-folders) for the directory) there needs to be a config.py file with the configuration keys:

Some key that are needed:

- [SECRET_KEY](https://flask.palletsprojects.com/en/2.3.x/config/#SECRET_KEY)

- [SQLALCHEMY_DATABASE_URI](https://flask-sqlalchemy.palletsprojects.com/en/3.0.x/config/#flask_sqlalchemy.config.SQLALCHEMY_DATABASE_URI)

## Execution

The Code can be use for development and testing via a convenient wrapper as shown bellow

```bash
expense run
```

In production its recommended to use WGSI server like gunicorn.
To use with gunicorn run:

```bash
gunicorn 'expense:create_app()'
```
