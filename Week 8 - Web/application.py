# -*- coding: utf-8 -*-
"""
Created on Fri Jul 24 12:25:37 2020

@author: simon
"""

# export API_KEY=pk_e2b4fc142db74747865eff7c4f1bbb4d
import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
import math
import datetime

from helpers import apology, login_required, lookup, usd

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

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

# Make sure API key is set
#if not os.environ.get("API_KEY"):
#    raise RuntimeError("API_KEY not set")


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""

    # Load Portfolio Database
    portfolio = db.execute("SELECT * FROM portfolio WHERE id=?", session["user_id"])

    # Add Current Price and Position Values to Portfolio
    for position in portfolio:
        px = lookup(position['ticker'])['price']
        position["mkt_px"] = px
        position["mkt_value"] = round(px * position["position"], 2)
        position["p&l"] = round(position["mkt_value"] - position["cost_value"], 2)
        position["p&l%"] = round(position["p&l"] / position["cost_value"] * 100, 2)

    # Compute Portfolio Totals
    port_mkt_val = round( sum([position["mkt_value"] for position in portfolio]), 2)
    port_pnl = round( sum([position["p&l"] for position in portfolio]), 2)
    port_cost_val = round( sum([position["cost_value"] for position in portfolio]), 2)
    if port_cost_val == 0:
        port_pnl_pct = 0
    else:
        port_pnl_pct = round(port_pnl / port_cost_val * 100, 2)

    # Load the Current Cash Balance For The User
    cash = db.execute("SELECT * FROM users WHERE id=?", session["user_id"])
    cash = round(cash[0]["cash"], 2)

    # Load the Portfolio Screen
    return render_template("portfolio.html", rows=portfolio, cash=cash, port_mkt_val=port_mkt_val, port_pnl=port_pnl, port_pnl_pct=port_pnl_pct)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure a Ticker was submitted
        if not request.form.get("ticker"):
            return apology("must provide a ticker", 403)

        # Lookup the Stock Ticker
        stock_data = lookup(request.form.get("ticker"))

        # Store Trade Data for easy reference
        name = stock_data['name']
        price = stock_data['price']
        ticker = stock_data['symbol']
        quantity = int(request.form.get("quantity"))
        cost_value = round(price * quantity, 2)
        date = datetime.datetime.now()

        # Check Ticker was valid
        if stock_data == None:
            return apology("ticker is not valid", 403)

        # Ensure a Quantity was submitted
        if not quantity:
            return apology("must provide a quantity " , 403)

        # Check user can afford the purchase
        rows = db.execute("SELECT * FROM users WHERE id= :id", id=session["user_id"])
        balance = rows[0]["cash"]
        if balance < cost_value:
            return apology("you cannot afford this purchase. You can only afford " + str(int(balance/price)) + " shares.", 403)

        # Add purchase to users trade history
        #CREATE TABLE IF NOT EXISTS 'history'
        #    (
        #        'id' INTEGER NOT NULL,
        #        'ticker' TEXT NOT NULL,
        #        'name' TEXT NOT NULL,
        #        'direction' TEXT NOT NULL,
        #        'quantity' NUMERIC NOT NULL,
        #        'price' NUMERIC NOT NULL,
        #        'date' DATE NOT NULL
        #    );

        db.execute("INSERT INTO history (id, ticker, name, direction, quantity, price, date) VALUES (:id, :ticker, :name, :direction, :quantity, :price, :date)",
                    id=session["user_id"],
                    ticker=ticker,
                    name=name,
                    direction="buy",
                    quantity=quantity,
                    price=price,
                    date=date)

        # Add purchase to users portfolio
        #CREATE TABLE IF NOT EXISTS 'portfolio'
        #    (
        #        'id' INTEGER NOT NULL,
        #        'ticker' TEXT NOT NULL,
        #        'name' TEXT NOT NULL,
        #        'position' NUMERIC NOT NULL,
        #        'cost_px' NUMERIC NOT NULL,
        #        'cost_value' NUMERIC NOT NULL
        #    );

        portfolio = db.execute("SELECT * from portfolio WHERE (id= :id AND ticker= :ticker)",
                            id=session["user_id"],
                            ticker=ticker)

        # If Position Already Exists, then New Values Must Be Calculated
        if len(portfolio) > 0:

            current_position = portfolio[0]["position"]
            current_price = portfolio[0]["cost_px"]
            new_position = current_position + quantity
            avg_cost_px = round((current_position * current_price + quantity * price) / new_position, 2)
            new_cost_val = round(avg_cost_px * new_position, 2)

            db.execute("UPDATE portfolio SET position=?, cost_px=?, cost_value=? WHERE (id=? AND ticker=?)",(
                        new_position,
                        avg_cost_px,
                        new_cost_val,
                        session["user_id"],
                        ticker))

        # If Position Does Not Exist, then Add New Trade to Portfolio Table
        else:
            db.execute("INSERT INTO portfolio (id, ticker, name, position, cost_px, cost_value) VALUES (:id, :ticker, :name, :position, :cost_px, :cost_value)",
                        id=session["user_id"],
                        ticker=ticker,
                        name=name,
                        position=quantity,
                        cost_px=price,
                        cost_value=cost_value)

        # Decrement Users Cash Balance
        db.execute("UPDATE users SET cash=? WHERE id=?",(balance - cost_value, session["user_id"]))

        # Show the stock data on a screen to check it...
        return render_template("buy.html", name=name, price=price, ticker=ticker, quantity=quantity)


    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""

    # Load Portfolio Database
    history = db.execute("SELECT * FROM history WHERE id=? ORDER BY date DESC ", session["user_id"])

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
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure a Ticker was submitted
        if not request.form.get("ticker"):
            return apology("must provide a ticker", 403)

        # Lookup the Stock Ticker
        stock_data = lookup(request.form.get("ticker"))

        # Check Ticker was valid
        if stock_data == None:
            return apology("ticker is not valid", 403)

        name = stock_data['name']
        price = usd(stock_data['price'])
        symbol = stock_data['symbol']
        peRatio = stock_data['peRatio']
        bid = stock_data['bid']
        ask = stock_data['ask']

        # Show the stock data on a screen to check it...
        return render_template("quote.html", name=name, price=price, symbol=symbol, peRatio=peRatio, bid=bid, ask=ask)

        # User Clicks Bid / Offer Buttons...
        buy = request.form.get("buy")
        sell = request.form.get("sell")


    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("quote.html")


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


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure a Ticker was submitted
        if not request.form.get("ticker"):
            return apology("must provide a ticker", 403)

        # Lookup the Stock Ticker
        stock_data = lookup(request.form.get("ticker"))

        # Store Trade Data for easy reference
        name = stock_data['name']
        price = stock_data['price']
        ticker = stock_data['symbol']
        quantity = int(request.form.get("quantity"))
        sell_value = price * quantity
        date = datetime.datetime.now()

        # Check Ticker was valid
        if stock_data == None:
            return apology("ticker is not valid", 403)

        # Ensure a Quantity was submitted
        if not quantity:
            return apology("must provide a quantity " , 403)

        # Add purchase to users trade history

        #CREATE TABLE IF NOT EXISTS 'history'
        #    (
        #        'id' INTEGER NOT NULL,
        #        'ticker' TEXT NOT NULL,
        #        'name' TEXT NOT NULL,
        #        'direction' TEXT NOT NULL,
        #        'quantity' NUMERIC NOT NULL,
        #        'price' NUMERIC NOT NULL,
        #        'date' DATE NOT NULL
        #    );

        db.execute("INSERT INTO history (id, ticker, name, direction, quantity, price, date) VALUES (:id, :ticker, :name, :direction, :quantity, :price, :date)",
                    id=session["user_id"],
                    ticker=ticker,
                    name=name,
                    direction="sell",
                    quantity=quantity,
                    price=price,
                    date=date)

        # Update Portfolio

        #CREATE TABLE IF NOT EXISTS 'portfolio'
        #    (
        #        'id' INTEGER NOT NULL,
        #        'ticker' TEXT NOT NULL,
        #        'name' TEXT NOT NULL,
        #        'position' NUMERIC NOT NULL,
        #        'cost_px' NUMERIC NOT NULL,
        #        'cost_value' NUMERIC NOT NULL
        #    );

        # Retrieve the users current portfolio
        portfolio = db.execute("SELECT * from portfolio WHERE (id= :id AND ticker= :ticker)", id=session["user_id"], ticker=ticker)

        current_position = portfolio[0]["position"]
        current_price = portfolio[0]["cost_px"]
        new_position = current_position - quantity

        # If new_position is zero, delete from portfolio, else decrement position
        if new_position == 0:
            db.execute("DELETE FROM portfolio WHERE (id= :id AND ticker= :ticker)", id=session["user_id"], ticker=ticker)
        else:
            avg_cost_px = (current_position * current_price - quantity * price) / new_position
            db.execute("UPDATE portfolio SET position=?, cost_px=? WHERE (id=? AND ticker=?)",(
                        new_position,
                        avg_cost_px,
                        session["user_id"],
                        ticker))

        # Increment Users Cash Balance
        user = db.execute("SELECT * FROM users WHERE id=?", session["user_id"])
        balance = user[0]["cash"]
        db.execute("UPDATE users SET cash=? WHERE id=?",(balance + sell_value, session["user_id"]))

        # Show the trade confirmation on a screen to check it was successful...
        return render_template("sell.html", name=name, price=price, ticker=ticker, quantity=quantity)

    # User reached route via GET (as by clicking a link or via redirect)
    else:

        # Find the Stocks the User Currently Holds
        stocks_held = db.execute("SELECT ticker FROM portfolio WHERE id= :id", id=session["user_id"])

        # Load Sell Ticket Page
        return render_template("sell.html", rows=stocks_held)



def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
