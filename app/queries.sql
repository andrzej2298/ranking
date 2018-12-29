-- all countries
SELECT name, code
FROM countries;

-- current position
SELECT rank
FROM current_ranking
WHERE code = 'POL';

-- highest position
SELECT rank, date
FROM ranking
WHERE code = 'POL'
AND rank = (
    SELECT MIN(rank)
    FROM ranking
    WHERE code = 'POL');

-- lowest position
SELECT rank, date
FROM ranking
WHERE code = 'POL'
AND rank = (
    SELECT MAX(rank)
    FROM ranking
    WHERE code = 'POL');

-- all positions
SELECT rank, date
FROM ranking
WHERE code = 'POL'
ORDER BY date;

-- position in federation
WITH current_confederation AS (
    SELECT code, rank
    FROM current_ranking
    WHERE confederation = (
        SELECT confederation
        FROM current_ranking
        WHERE code = 'POL'
    )
)
SELECT COUNT(code) + 1 AS rank
FROM current_confederation
WHERE rank < (
    SELECT rank
    FROM current_confederation
    WHERE code = 'POL'
);

-- current ranking for the choropleth
SELECT countries.name AS name, current_ranking.rank AS rank
FROM countries
JOIN current_ranking
ON countries.code = current_ranking.code;

-- biggest winners (losers)
WITH current_countries AS (
    SELECT current_ranking.code AS code,
    countries.name AS name
    FROM current_ranking
    JOIN countries
    ON current_ranking.code = countries.code
)
SELECT current_countries.name, SUM(ranking.movement) AS global_movement
FROM current_countries
JOIN ranking
ON current_countries.code = ranking.code
WHERE date >= '2018-01-01'
GROUP BY current_countries.code
ORDER BY global_movement asc
LIMIT 10;

-- confederation places in top n
SELECT confederation,
COUNT(confederation) AS occurrences
FROM ranking
WHERE rank <= n
GROUP BY confederation;

-- combine with GDP and population
SELECT name, usdmln AS gdp, rank, population
FROM countries
JOIN current_ranking
ON countries.code = current_ranking.code
JOIN gdp
ON countries.code = gdp.code
JOIN population
ON countries.code = population.code;

-- averages
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