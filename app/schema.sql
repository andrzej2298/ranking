.mode csv

DROP TABLE IF EXISTS ranking;
DROP TABLE IF EXISTS gdp;
DROP TABLE IF EXISTS population;
DROP TABLE IF EXISTS countries;

CREATE TABLE ranking (
  rank INTEGER NOT NULL CHECK(rank >= 0),
  code TEXT NOT NULL,
  points INTEGER NOT NULL CHECK(points >= 0),
  prevpoints INTEGER NOT NULL CHECK(prevpoints >= 0),
  movement INTEGER NOT NULL,
  confederation TEXT NOT NULL,
  date DATE NOT NULL
);

CREATE TABLE gdp (
  code TEXT PRIMARY KEY,
  usdmln INTEGER NOT NULL
);

CREATE TABLE population (
  code TEXT PRIMARY KEY,
  population INTEGER NOT NULL
);

CREATE TABLE countries (
  code TEXT PRIMARY KEY,
  name TEXT NOT NULL
);

.import data/population.csv population
.import data/ranking.csv ranking
.import data/gdp.csv gdp
.import data/countries.csv countries
