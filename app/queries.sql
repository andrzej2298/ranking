-- wszystkie państwa (potrzebne do menu, żeby wybrać państwo)
SELECT name, code
FROM countries;


--------------------------------------------
-- informacje o pojedynczej reprezentacji --
--------------------------------------------

-- miejsce 
SELECT rank
FROM current_ranking
WHERE code = '{code}';

-- najwyższe i najniższe miejsce w historii
        SELECT DISTINCT rank, strftime('%Y', date) AS year
        FROM ranking
        WHERE code = '{code}'
        AND rank = (
            SELECT {function}(rank)
            FROM ranking
            WHERE code = '{code}')
        ORDER BY date;
-- miejsce na tle federacji
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

-- wszystkie historyczne miejsca w rankingu
        SELECT rank, date
        FROM ranking
        WHERE code = '{code}'
        ORDER BY date;


--------------------------------------------
------------ informacje ogólne -------------
--------------------------------------------

-- aktualny ranking
SELECT countries.name AS name, current_ranking.rank AS rank
FROM countries
JOIN current_ranking
ON countries.code = current_ranking.code
ORDER BY rank;

-- dla każdej federacji informacja, ile razy
-- państwo z niej było na jednym z n pierwszych miejsc
SELECT confederation,
COUNT(confederation) AS occurrences
FROM ranking
WHERE rank <= {n}
GROUP BY confederation;

-- dla państw z aktualnego rankingu informacja
-- o miejscu w rankingu, PKB oraz populacji
-- do wyliczenia rankingu biorącego pod uwagę
-- te wskaźniki
SELECT name, usdmln AS gdp, rank, population
FROM countries
JOIN current_ranking
ON countries.code = current_ranking.code
JOIN gdp
ON countries.code = gdp.code
JOIN population
ON countries.code = population.code;

-- średnie miejsce w rankingu, zamiast
-- prognozy rankingu na następne zestawienie
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

-- najlepsze/najgorsze 10 reprezentacji w 2018
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