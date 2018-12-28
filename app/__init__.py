from flask import Flask
from app.db import close_db
from config import Config


app = Flask(__name__)
app.config.from_object(Config)
app.teardown_appcontext(close_db)

from app import routes
