#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#

# imports
import psycopg2
import bleach


# function of the app tournament
def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Remove all the match records from the database."""
    DB = connect()
    conn = DB.cursor()
    conn.execute("DELETE FROM matches")
    DB.commit()
    DB.close()


def deletePlayers():
    """Remove all the player records from the database."""
    DB = connect()
    conn = DB.cursor()
    conn.execute("DELETE FROM players")
    DB.commit()
    DB.close()


def countPlayers():
    """Returns the number of players currently registered."""
    DB = connect()
    conn = DB.cursor()
    conn.execute("SELECT count(id_player) FROM players")
    c = conn.fetchone()[0]
    return c
    DB.close()


def registerPlayer(player_name):
    """Adds a player to the tournament database.

    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)

    Args:
      name: the player's full name (need not be unique).
    """
    DB = connect()
    conn = DB.cursor()
    name = bleach.clean(player_name)
    conn.execute("INSERT INTO players (player_name) VALUES (%s)",
                 (player_name,))
    DB.commit()
    DB.close()


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.
    The first entry in the list should be the player in first place,
    or a player tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    DB = connect()
    conn = DB.cursor()
    conn.execute("SELECT * FROM playerstanding")
    result = conn.fetchall()
    DB.close()
    return result


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    DB = connect()
    conn = DB.cursor()
    winner = bleach.clean(winner)
    loser = bleach.clean(loser)
    conn.execute("INSERT INTO matches (winner, loser) VALUES (%s, %s);",
                 (winner, loser,))
    DB.commit()
    DB.close()


def swissPairings():
    """Returns a list of pairs of players for the next round of a match.
    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.

    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    # SQL SELECTS
    DB = connect()
    conn = DB.cursor()

    conn.execute("SELECT winner, loser FROM matches")
    con = conn.fetchall()

    conn.execute("SELECT id_player FROM wins")
    con2 = conn.fetchall()

    conn.execute("SELECT id_player, player_name FROM wins")
    req = conn.fetchall()

    # We define vars, lists and init them
    n = 0
    a = 0
    b = 1
    c = 0
    result = []
    temp = []
    size = len(req)
    checksize = len(con)

    if size < 2:
        raise ValueError("just 1 player, please add at least one other")

    while n < size:
        prob = False
        while prob is False and c < checksize:
            if ((con[c] == (con2[a] + con2[b])) or 
                (con[c] == (con2[b] + con2[a]))):
                b = b + 1
                prob = False
            else:
                prob = True
            c = c + 1
        temp = req[a] + req[b]
        result.append(temp)
        n = n+2
        a = a + 2
        b = a + 1
    return result
    DB.close()
