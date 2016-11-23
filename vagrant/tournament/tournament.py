#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Remove all the match records from the database."""
    db = connect()
    c = db.cursor()
    c.execute("DELETE FROM matches")
    c.commit()
    db.close()

def deletePlayers():
    """Remove all the player records from the database."""
    db = connect()
    c = db.cursor()
    c.execute("DELETE FROM players")
    c.commit()
    db.close()

def countPlayers():
    """Returns the number of players currently registered."""
    db = connect()
    c = db.cursor()
    c.execute("SELECT COUNT(*) FROM players")
    row = c.fetchone()
    db.close()
    return row

def getPlayerName(id):
    """Returns the name of the player based on the ID."""
    db = connect()
    c = db.cursor()
    c.execute("SELECT name FROM players where p_id=(%s)",(name,))
    row = c.fetchone()
    db.close()
    return row


def registerPlayer(name):
    """Adds a player to the tournament database.

    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)

    Args:
      name: the player's full name (need not be unique).
    """
    db = connect()
    db.execute("INSERT INTO players (NAME) VALUES (%s)",(name,))
    db.commit()
    db.close()

def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    sSQL = "SELECT players.id as pid,(p1_count + p2_count) as matches, wins.count_wins as W \
    FROM players left join \
    (SELECT p1_id as p_id,COUNT(p1_id) as n_matches FROM matches GROUP BY p1_id) AS p1_count \
     ON players.id = p1_count.p1_id join \
    (SELECT p2_id as p_id,COUNT(p2_id) as n_matches FROM matches GROUP BY p2_id) AS p2_count \
    on p1_count.p1_id = p2_count.p2_id join \
    (SELECT w as p_id,COUNT(w) as count_wins FROM matches GROUP BY w) AS wins \
    on p2_count.p2_id = wins.w \
    WHERE p2_count.p_id = p1_count.p_id and players.id=p2_count.p_id \
    ORDER BY w"


    db = connect()
    c = db.cursor()
    c.execute(sSQL)
    rows = c.fetchall()
    db.close()
    return rows


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    db = connect()
    c = db.cursor()
    db.execute("INSERT INTO matches (winner,loser) values (%s)",(winner,loser))
    db.commit()
    db.close()

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
    stand = playerStandings()
    nCount = 1
    lst = []

    name = ""
    for player in stand:
        name = getPlayerName(player[0])
        if nCount % 2 == 0:
            tempTuple = tempTuple + (player[0],name)
            list[nCount/2 - 1] = tempTuple
        else:
            tempTuple = (player[0],name)
        nCount = nCount + 1
    return list

