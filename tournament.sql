-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.


-- creation of the tables

-- players

DROP DATABASE tournament;
CREATE DATABASE tournament;
\c tournament;


CREATE TABLE players (
    id_player    				      serial,
    player_name                       varchar(80),
	CONSTRAINT PK_p PRIMARY KEY		  (id_player)
);

-- matches

CREATE TABLE matches (
 	id_match    				      serial,
    winner         					  int NOT NULL references players(id_player),
 	loser          					  int NOT NULL references players(id_player),
	CONSTRAINT PK_m PRIMARY KEY		  (id_match)
);

-- creation of the views

CREATE VIEW	wins AS
	SELECT players.id_player, players.player_name, count(matches.winner) AS wins
	FROM players LEFT JOIN matches ON players.id_player = matches.winner
	GROUP BY players.id_player
	ORDER BY wins DESC;

CREATE VIEW	loss AS
	SELECT players.id_player, players.player_name, count(matches.loser) AS loss
	FROM players LEFT JOIN matches ON players.id_player = matches.loser
	GROUP BY players.id_player;


CREATE VIEW playerstanding AS
	SELECT players.id_player, players.player_name, wins.wins, loss+wins as matches 
	FROM players,Wins,loss 
	WHERE players.id_player = wins.id_player and wins.id_player = loss.id_player;



