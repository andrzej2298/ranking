.mode csv

DROP TABLE IF EXISTS ranking;
DROP TABLE IF EXISTS gdp;
DROP TABLE IF EXISTS population;
DROP TABLE IF EXISTS countries;

CREATE TABLE countries (
  code TEXT PRIMARY KEY CHECK(length(code) = 3),
  name TEXT NOT NULL
);

CREATE TABLE ranking (
  rank INTEGER NOT NULL CHECK(rank >= 0),
  code TEXT NOT NULL,
  points INTEGER NOT NULL CHECK(points >= 0),
  confederation TEXT NOT NULL,
  date DATE NOT NULL,
  PRIMARY KEY(code, date),
  FOREIGN KEY(code) REFERENCES countries(code)
);

CREATE TABLE gdp (
  code TEXT PRIMARY KEY,
  usdmln INTEGER NOT NULL CHECK(usdmln >= 0),
  FOREIGN KEY(code) REFERENCES countries(code)
);

CREATE TABLE population (
  code TEXT PRIMARY KEY,
  population INTEGER NOT NULL CHECK(population >= 0),
  FOREIGN KEY(code) REFERENCES countries(code)
);

.import data/countries.csv countries
.import data/population.csv population
.import data/ranking.csv ranking
.import data/gdp.csv gdp

DROP VIEW IF EXISTS current_ranking;
CREATE VIEW current_ranking AS
SELECT rank, code, points, confederation, date
FROM ranking
WHERE date = (SELECT MAX(date) FROM ranking);
