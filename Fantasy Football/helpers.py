import os
import requests
import urllib.parse
from cs50 import SQL
import sqlite3
import pandas as pd
import ssl
import json
from urllib3 import poolmanager

from flask import redirect, render_template, request, session
from functools import wraps

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///football.db")

def apology(message, code=400):
    """Render message as an apology to user."""
    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [("-", "--"), (" ", "-"), ("_", "__"), ("?", "~q"),
                         ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]:
            s = s.replace(old, new)
        return s
    return render_template("apology.html", top=code, bottom=escape(message)), code


def login_required(f):
    """
    Decorate routes to require login.

    http://flask.pocoo.org/docs/1.0/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function


def loadPlayerData():
    '''
    Scrapes the player data from the Telegraph website and stores it into the 'players' database.
    '''

    # workaround to avoid SSL errors:
    class TLSAdapter(requests.adapters.HTTPAdapter):
        def init_poolmanager(self, connections, maxsize, block=False):
            """Create and initialize the urllib3 PoolManager."""
            ctx = ssl.create_default_context()
            ctx.set_ciphers('DEFAULT@SECLEVEL=1')
            self.poolmanager = poolmanager.PoolManager(
                    num_pools=connections,
                    maxsize=maxsize,
                    block=block,
                    ssl_version=ssl.PROTOCOL_TLS,
                    ssl_context=ctx)

    # Fetch data from here
    url = 'https://fantasyfootball.telegraph.co.uk/premier-league/json/getstatsjson'

    # Request the data
    session = requests.session()
    session.mount('https://', TLSAdapter())

    # data is a dictionary of lists of dictionaries
    data = session.get(url).json()

    # df is a pandas dataframe
    df = pd.DataFrame(data['playerstats'])

    # connect to the database
    connection = sqlite3.connect("football.db")

    # convert the dataframe into an sql table
    df.to_sql('players', con=connection, if_exists='replace')


def makeBid(userid, playerid, px_bid):

    # Check user can afford the purchase
    rows = db.execute("SELECT * FROM users WHERE id=?", userid)
    balance = rows[0]["cash"]
    if balance < px_bid:
        return apology("you cannot afford this purchase.", 403)

    # Find the players the current user has already bid on.
    playerlist = db.execute("SELECT playerid FROM bidlist WHERE userid=?", userid)

    for p in playerlist:
        # If the user has previous bid on this player..
        if str(playerid) == str(p['playerid']):
            # Check the current bid price
            current_bid = db.execute("SELECT * FROM portfolio WHERE userid=? AND playerid=?", userid, playerid)[0]['cost_px']
            # REPLACE the existing bidlist record with the new bid
            db.execute("UPDATE bidlist SET px_bid=? WHERE userid=? AND playerid=?", px_bid, userid, playerid)
            # REPLACE the existing portfolio record with the new bid
            db.execute("UPDATE portfolio SET cost_px=? WHERE userid=? AND playerid=?", px_bid, userid, playerid)
            # Decrement cash balance
            balance = db.execute("SELECT * FROM users WHERE id=?", userid)[0]['cash']
            new_balance = round(float(balance) - (float(px_bid) - float(current_bid)), 2)
            db.execute("UPDATE users SET cash=? WHERE id=?", new_balance, userid)
            break
    # The user has NOT previous bid on this player...
    else:
        # ADD the Bid to the Bid List
        db.execute("INSERT INTO bidlist (userid, playerid, px_bid) VALUES (:userid, :playerid, :px_bid)", userid=userid, playerid=playerid, px_bid=px_bid)
        # ADD the Bid to the users portfolio
        db.execute("INSERT INTO portfolio (userid, playerid, cost_px) VALUES (:userid, :playerid, :cost_px)", userid=userid, playerid=playerid, cost_px=px_bid)
        # Decrement cash balance
        balance = db.execute("SELECT * FROM users WHERE id=?", userid)[0]['cash']
        new_balance = round(float(balance) - float(px_bid), 2)
        db.execute("UPDATE users SET cash=? WHERE id=?", new_balance, userid)
