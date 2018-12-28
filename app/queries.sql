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