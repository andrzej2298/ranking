from app.db import get_db


def simple_query():
    cur = get_db().cursor()
    result = []
    for e in cur.execute('select name from countries;'):
        print(e['name'])
        result.append(e['name'])
    return result
