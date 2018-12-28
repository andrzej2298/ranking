import sqlite3

from flask import g


# def get_db():
#     if not hasattr(g, 'sqlite_db'):
#         g.sqlite_db = sqlite3.connect('database.sqlite')
#         g.sqlite_db.row_factory = sqlite3.Row
#     return g.db


# def close_db(e=None):
#     if hasattr(g, 'sqlite_db'):
#         g.sqlite_db.close()

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
