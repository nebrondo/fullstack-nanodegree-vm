-- Table definitions for the tournament project.
--
CREATE TABLE players (
    p_id SERIAL PRIMARY KEY,
    NAME VARCHAR(50)
);

CREATE TABLE tournament (
    t_id SERIAL PRIMARY KEY,
    NAME VARCHAR(50)
);

CREATE TABLE matches (
    m_id SERIAL PRIMARY KEY,
    t_id integer REFERENCES tournament,
    p1_id integer REFERENCES players,
    p2_id integer REFERENCES players,
    winner integer REFERENCES players,
    loser integer REFERENCES players
);


SELECT p1_count.p_id as pid,(p1_count.n_matches + p2_count.n_matches) as matches, wins.count_wins as W
    FROM
    (SELECT p_id,COUNT(p1_id) as n_matches
        FROM players left join matches on players.p_id = matches.p1_id
        GROUP BY players.p_id) AS p1_count
    left join
    (SELECT p_id,COUNT(p2_id) as n_matches
        FROM players left join matches on players.p_id = matches.p2_id
        GROUP BY players.p_id) AS p2_count
    on p1_count.p_id = p2_count.p_id left join
    (SELECT players.p_id as p_id,COUNT(winner) as count_wins
        FROM players left join matches on players.p_id = matches.winner
        GROUP BY players.p_id) AS wins
    on p2_count.p_id = wins.p_id
    ORDER BY W DESC,p1_count.p_id;
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.


