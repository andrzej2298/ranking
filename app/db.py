import sqlite3

from flask import g


def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect('database.sqlite')
        g.db.row_factory = sqlite3.Row
    return g.db


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()


