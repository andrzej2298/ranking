from flask import render_template
from app import app
from app.queries import simple_query


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', content=simple_query())
