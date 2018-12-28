from app.db import get_db

queries = {
    'all_countries': """
        SELECT name, code
        FROM countries;
    """,
    'current_rank': """
        SELECT rank
        FROM current_ranking
        WHERE code = '{code}';
    """,
    'min_max': """
        SELECT rank, date
        FROM ranking
        WHERE code = '{code}'
        AND rank = (
            SELECT {function}(rank)
            FROM ranking
            WHERE code = '{code}');
    """,
    'federation_rank': """
        WITH current_confederation AS (
            SELECT code, rank
            FROM current_ranking
            WHERE confederation = (
                SELECT confederation
                FROM current_ranking
                WHERE code = '{code}'
            )
        )
        SELECT COUNT(code) + 1 AS rank
        FROM current_confederation
        WHERE rank < (
            SELECT rank
            FROM current_confederation
            WHERE code = '{code}'
        );
    """
}


def query(query):
    cur = get_db().cursor()
    return cur.execute(query)


def all_countries():
    queried = query(queries['all_countries'])
    return [('', '')] + [(entry['code'], entry['name']) for entry
                         in queried]


def current_rank(code):
    queried = query(queries['current_rank'].format(code=code))
    result = [entry['rank'] for entry in queried]
    assert(len(result) == 1)
    return result[0]


def plays_currently(code):
    queried = query(queries['current_rank'].format(code=code))
    result = [entry['rank'] for entry in queried]
    assert(len(result) == 1 or len(result) == 0)
    return len(result) == 1


def mins_and_maxes(code):
    mins = query(queries['min_max'].format(code=code, function='MIN'))
    maxes = query(queries['min_max'].format(code=code, function='MAX'))
    min_results = [{'date': entry['date'], 'rank': entry['rank']}
                   for entry in mins]
    max_results = [{'date': entry['date'], 'rank': entry['rank']}
                   for entry in maxes]
    return {'mins': min_results, 'maxes': max_results}


def current_federation_rank(code):
    queried = query(queries['federation_rank'].format(code=code))
    result = [entry['rank'] for entry in queried]
    assert(len(result) == 1)
    return result[0]

