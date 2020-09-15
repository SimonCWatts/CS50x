import os
from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
import sqlite3
from helpers import apology, login_required, loadPlayerData, makeBid
import pandas as pd

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///football.db")

# Download & Update the 'players' database from the Telegraph website
loadPlayerData()

@app.route("/")
def index():
    """Welcome the players"""
    try:
        name = db.execute("SELECT * FROM users WHERE id=?", session['user_id'])
        return render_template("home.html", name = name[0]['username'])
    except KeyError:
        return render_template("home.html")
    except NameError:
        return render_template("home.html")


@app.route("/bid", methods=["GET", "POST"])
@login_required
def bid():
    """Bid for a Player"""

    if request.method == "POST":

        # Ensure a Player was submitted
        if not request.form.get("playerName"):
            return apology("must provide a Player's Name", 403)

        # Ensure a Bid Price was submitted
        if not request.form.get("px_bid"):
            return apology("must provide a Bid Price " , 403)

        # Find corresponding player data from the database
        player = db.execute("SELECT * FROM players WHERE PLAYERFULLNAME = ?", request.form.get("playerName"))
        playerid = player[0]['PLAYERID']

        # Retrieve the BID price from the form
        px_bid = float(request.form.get("px_bid"))

        # Enter Bid
        makeBid(session['user_id'], playerid, px_bid)

        # Find the names of all the Players in the league
        players = db.execute("SELECT * FROM players ORDER BY PLAYERFULLNAME")

        # Show the Player data on a screen to confirm the bid
        return render_template("bid.html", rows=players, name=player[0]['PLAYERFULLNAME'], price=request.form.get("px_bid"))

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        # Find the names of all the Players in the league
        players = db.execute("SELECT * FROM players ORDER BY PLAYERFULLNAME")
        # Allow the user to choose the player they want to bid for via a drop down menu
        return render_template("bid.html", rows=players)


@app.route("/history", methods=["GET"])
@login_required
def history():
    """Show history of bids made for a single player"""

    if request.method == "GET":

        # Obtain the Playerid from the parameters submitted when calling the function
        playerid=request.args.get("playerid")

        # Obtain bid history for player
        history=db.execute(""" SELECT * FROM bidlist
                                        LEFT JOIN users ON bidlist.userid = users.id
                                        LEFT JOIN players ON bidlist.playerid = players.PLAYERID
                                        WHERE bidlist.playerid=?
                                        ORDER BY bidlist.px_bid DESC""", playerid)

        # Show the history in a table
        return render_template("history.html", rows=history)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return render_template("home.html", name = rows[0]['username'])

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")

@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return render_template("home.html")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get Player Data."""
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # If user has clicked 'Buy!'
        if 'bid_button' in request.form:

            # Set Bid = True
            bid=True

            # Player ID taken from the button value
            playerid = request.form["bid_button"]
            player_data = db.execute("SELECT * FROM players WHERE PLAYERID =?", playerid)

            # get the submitted data from the page
            px_bid = float(request.form.get("px_bid"))

            # Enter Bid
            makeBid(session['user_id'], playerid, px_bid)

        else:
            # Get the player name from the form
            name = request.form.get("playerName")

            # Set Bid = False
            bid=False

            # Lookup the Player Data
            player_data = db.execute("SELECT * FROM players WHERE PLAYERFULLNAME=?", name)

        # Show the Player data to the user
        return render_template("quote.html", player=player_data, bid=bid)

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        players = db.execute("SELECT * FROM players ORDER BY PLAYERFULLNAME")
        return render_template("quote.html", rows=players)


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Ensure passwords are identical
        elif request.form.get("password") != request.form.get("confirm_password") :
            return apology("passwords must match", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # Ensure username does not already exist
        if len(rows) != 0 :
            return apology("user name already exists", 403)

        # Hash the password
        pw_hash = generate_password_hash(request.form.get("password"), method='pbkdf2:sha256', salt_length=8)

        # Insert the new user into the "users" table
        db.execute("INSERT INTO users (username, hash) VALUES (:username, :pw_hash)",
                    username=request.form.get("username"), pw_hash=pw_hash)

        # Return user to login page
        return redirect("/login")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")


@app.route("/offer", methods=["GET", "POST"])
@login_required
def offer():
    """Sell players that you own"""

    # Find the names of the Players the User owns
    myPlayers = db.execute("""  SELECT *
                                FROM players
                                LEFT JOIN portfolio ON players.PLAYERID = portfolio.playerid
                                WHERE portfolio.userid = :id"""
                              , id = session['user_id'])

    return render_template("offer.html", rows=myPlayers)


@app.route("/portfolio")
@login_required
def portfolio():
    """Show portfolio of players"""

    # Load Portfolio, Players & User Database
    rows = db.execute("""SELECT * FROM portfolio
                        LEFT JOIN players ON portfolio.playerid = players.PLAYERID
                        LEFT JOIN users on portfolio.userid = users.id
                        WHERE users.id =?
                        ORDER BY players.POS""",
                        session['user_id'])

    # Compute the value of all players in portfolio
    port_val = db.execute("SELECT SUM(cost_px) FROM portfolio WHERE userid=?", session['user_id'])[0]['SUM(cost_px)']

    if len(rows) != 0:
        # Load the Portfolio Screen
        return render_template("portfolio.html", rows=rows, pv=round(port_val,2))
    else:
        return render_template("portfolio.html")


@app.route("/directory")
@login_required
def directory():
    """Show all players"""

    # Load Players Database
    rows = db.execute("SELECT * FROM players ORDER BY players.POS")

    # If there is data, pass it into the HTML template
    if len(rows) != 0:
        return render_template("directory.html", rows=rows)
    else:
        return render_template("directory.html")


@app.route("/auction", methods=["GET", "POST"])
@login_required
def auction():
    """See Live Auction"""

    if request.method == "POST":

        # If the user clicks the 'Close Auction' button Then the player is allocated to the winning bidder...
        if 'close_button' in request.form:

            # Find the player who's auction was closed
            playerid = request.form['close_button']
            player = db.execute("SELECT * FROM players WHERE PLAYERID = ?", playerid)

            # Find the winning bid
            max_bid = db.execute("SELECT MAX(px_bid) FROM bidlist WHERE playerid=?", playerid)[0]['MAX(px_bid)']

            # Find winning bidder
            winning_bidder_id = db.execute("SELECT * FROM bidlist WHERE playerid=? AND px_bid=?", playerid, max_bid)[0]['userid']

            # Find the losing bidders
            losing_bidders = db.execute("SELECT * FROM bidlist WHERE playerid=? AND NOT userid=?", playerid, winning_bidder_id)

            # Add the cash back to each losing bidder
            for loser in losing_bidders:
                balance = db.execute("SELECT * FROM users WHERE id=?", loser['userid'])[0]['cash']
                losing_bid = db.execute("SELECT * FROM bidlist WHERE playerid=? AND userid=?", playerid, loser['userid'])[0]['px_bid']
                new_balance = round(float(balance) + float(losing_bid), 2)
                db.execute("UPDATE users SET cash=? WHERE id=?", new_balance, loser['userid'])

            # Set the status of the player to 'owned' in the winning players portfolio
            db.execute("UPDATE portfolio SET status='owned' WHERE playerid=? AND userid=?", playerid, session['user_id'])

            # Remove player from all others portfolios
            db.execute("DELETE FROM portfolio WHERE playerid=? AND NOT userid=?", playerid, winning_bidder_id)

            # Remove all player bids from bid list
            db.execute("DELETE FROM bidlist WHERE playerid=?", playerid)

        # The user has submitted a BID price and must be added to the auction
        else:
            # get the submitted data from the page
            playerid = request.form['bid_button']
            px_bid = float(request.form.get("px_bid"))

            # Find corresponding player data from the database
            player = db.execute("SELECT * FROM players WHERE PLAYERID = ?", playerid)

            # Make Bid
            makeBid(session['user_id'], playerid, px_bid)

    # Make a joined table from the BIDLIST, PLAYERS & USERS Databases
    rows = db.execute("""SELECT PLAYERFULLNAME, TEAMNAME, POS, VALUE, max(px_bid), username, userid, players.PLAYERID, count(px_bid)
                        FROM bidlist
                        LEFT JOIN players ON bidlist.playerid = players.PLAYERID
                        LEFT JOIN users ON bidlist.userid = users.id
                        GROUP BY PLAYERFULLNAME
                        ORDER BY players.PLAYERNAME, bidlist.px_bid DESC""")

    # Make a list of all the players the current user has bid on
    portfolio = db.execute("""SELECT playerid FROM portfolio WHERE userid=?""", session['user_id'])

    player_list = []
    for player in portfolio:
        player_list.append(player['playerid'])

    # Generate the Bid Table
    return render_template("auction.html", rows=rows, user=session['user_id'], port=player_list)


@app.route("/league", methods=["GET", "POST"])
@login_required
def league():
    """Show a league table of all the users"""

    # Make a joined table from the BIDLIST, PLAYERS & USERS Databases
    alldata = db.execute("""SELECT users.username, SUM(players.WEEKPOINTS), SUM(players.POINTS), users.cash
                            FROM portfolio
                            LEFT JOIN users ON portfolio.userid = users.id
                            LEFT JOIN players on portfolio.playerid = players.PLAYERID
                            GROUP BY users.username
                            ORDER BY SUM(players.POINTS) DESC;""")

    return render_template("league.html", rows=alldata)


@app.route("/topup", methods=["GET", "POST"])
@login_required
def topup():
    """Add Cash"""
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Get Top Up Quantity From Form
        quantity = int(request.form.get("topup"))

        # Get Current Cash Balance
        data = db.execute("SELECT * FROM users WHERE id=?", session["user_id"])
        cash = data[0]["cash"]

        # New Cash Balance
        new_balance = cash + quantity

        #add cash to portfolio
        db.execute("UPDATE users SET cash=? WHERE id=?", (new_balance, session["user_id"]))

        # Return user to the portfolio screen to confirm balance
        return redirect("/portfolio")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("topup.html")


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)