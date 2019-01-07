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
        SELECT DISTINCT rank, strftime('%Y', date) AS year
        FROM ranking
        WHERE code = '{code}'
        AND rank = (
            SELECT {function}(rank)
            FROM ranking
            WHERE code = '{code}')
        ORDER BY date;
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
    """,
    'all_ranks': """
        SELECT rank, date
        FROM ranking
        WHERE code = '{code}'
        ORDER BY date;
    """,
    'current_ranking': """
        SELECT countries.name AS name, current_ranking.rank AS rank
        FROM countries
        JOIN current_ranking
        ON countries.code = current_ranking.code
        ORDER BY rank;
    """,
    'top_places': """
        SELECT confederation,
        COUNT(confederation) AS occurrences
        FROM ranking
        WHERE rank <= {n}
        GROUP BY confederation;
    """,
    'gdp_and_population': """
        SELECT name, usdmln AS gdp, rank, population
        FROM countries
        JOIN current_ranking
        ON countries.code = current_ranking.code
        JOIN gdp
        ON countries.code = gdp.code
        JOIN population
        ON countries.code = population.code;
    """,
    'averages': """
        WITH current_countries AS (
            SELECT current_ranking.code AS code,
            countries.name AS name
            FROM current_ranking
            JOIN countries
            ON current_ranking.code = countries.code
        )
        SELECT current_countries.name
        FROM current_countries
        JOIN ranking
        ON current_countries.code = ranking.code
        GROUP BY current_countries.code
        ORDER BY AVG(ranking.rank);
    """,
    'movement': """
        WITH last_rank AS (
            SELECT code, rank
            FROM ranking
            WHERE date = (
                SELECT MAX(date) AS date
                FROM ranking
                WHERE date <= '2018-12-31'
            )
        ),
        first_rank AS (
            SELECT code, rank
            FROM ranking
            WHERE date = (
                SELECT MIN(date) AS date
                FROM ranking
                WHERE date >= '2018-01-01'
            )
        )
        SELECT countries.name,
        last_rank.rank - first_rank.rank AS global_movement
        FROM last_rank
        JOIN first_rank
        ON last_rank.code = first_rank.code
        JOIN countries
        ON last_rank.code = countries.code
        WHERE global_movement IS NOT NULL
        ORDER BY global_movement {mode}
        LIMIT 10;
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
    min_results = [{'year': entry['year'], 'rank': entry['rank']}
                   for entry in mins]
    max_results = [{'year': entry['year'], 'rank': entry['rank']}
                   for entry in maxes]
    return {'mins': min_results, 'maxes': max_results}


def current_federation_rank(code):
    queried = query(queries['federation_rank'].format(code=code))
    result = [entry['rank'] for entry in queried]
    assert(len(result) == 1)
    return result[0]


def all_ranks(code):
    queried = query(queries['all_ranks'].format(code=code))
    return [(entry['rank'], entry['date']) for entry in queried]


def current_ranking():
    queried = query(queries['current_ranking'])
    return [(entry['name'], entry['rank']) for entry in queried]


def top_places(n):
    queried = query(queries['top_places'].format(n=n))
    return [(entry['confederation'], entry['occurrences'])
            for entry in queried]


def gdp_and_population():
    queried = query(queries['gdp_and_population'])
    return [{
        'name': entry['name'],
        'gdp': entry['gdp'],
        'population': entry['population'],
        'rank': entry['rank']
    } for entry in queried]


def averages():
    queried = query(queries['averages'])
    countries = [entry['name'] for entry in queried]
    return [(i + 1, countries[i]) for i in range(0, min(len(countries), 30))]


def best_movement():
    queried = query(queries['movement'].format(mode='DESC'))
    return [(entry['name'], entry['global_movement']) for entry in queried]


def worst_movement():
    queried = query(queries['movement'].format(mode='ASC'))
    return [(entry['name'], entry['global_movement']) for entry in queried]
