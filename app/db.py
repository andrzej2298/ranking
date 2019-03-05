import sqlite3

from flask import g


def get_db():
    db = getattr(g, 'sqlite_database', None)
    if db is None:
        db = g._database = sqlite3.connect('database.sqlite')
        db.row_factory = sqlite3.Row
    return db


def close_db(exception):
    db = getattr(g, 'sqlite_database', None)
    if db is not None:
        db.close()
