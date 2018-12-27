from flask import Flask
from app.db import close_db


app = Flask(__name__)
app.teardown_appcontext(close_db)

from app import routes

