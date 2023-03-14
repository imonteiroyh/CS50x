import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")

# If table users is empty, reset index
if db.execute("SELECT COUNT(*) AS n FROM users")[0]["n"] == 0:
    db.execute("DELETE FROM sqlite_sequence WHERE name = 'users'")

# Create transactions table
if not len(db.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='transactions'")):
    db.execute("CREATE TABLE transactions (id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER, symbol TEXT NOT NULL, name TEXT NOT NULL, shares INTEGER NOT NULL, price NUMERIC NOT NULL, timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)")
    db.execute("CREATE UNIQUE INDEX id ON transactions (id)")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""

    user_stocks = db.execute("\
                             SELECT symbol, name, SUM(shares) AS shares FROM transactions WHERE user_id = ? GROUP BY symbol", session["user_id"])

    prices = {}
    total = 0
    if len(user_stocks):
        for stock in user_stocks:
            search = lookup(stock["symbol"])
            total += search["price"] * stock["shares"]
            prices[stock["symbol"]] = {"price": usd(search["price"]), "total": usd(search["price"] * stock["shares"])}

    cash = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])[0]["cash"]
    total += cash

    return render_template("index.html", stocks=user_stocks, prices=prices, cash=usd(cash), total=usd(total))


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "POST":
        symbol = request.form.get("symbol")
        if not symbol:
            return apology("must provide symbol")

        search = lookup(symbol)
        if not bool(search):
            return apology("invalid symbol")

        shares = request.form.get("shares")
        if not shares.isnumeric() or int(shares) == 0:
            return apology("shares must be a positive integer")

        total = int(shares) * search["price"]
        current_cash = db.execute("SELECT * FROM users WHERE id = ?", session["user_id"])[0]["cash"]

        if current_cash < total:
            return apology("insuficient cash")

        current_cash -= total

        db.execute("INSERT INTO transactions (user_id, symbol, name, shares, price) VALUES (?, ?, ?, ?, ?)",
                   session["user_id"], search["symbol"], search["name"], int(shares), search["price"])
        db.execute("UPDATE users SET cash = ? WHERE id = ?", current_cash, session["user_id"])

        flash("Bought!")
        return redirect("/")

    return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""

    transactions = db.execute("\
                              SELECT symbol, shares, price, timestamp FROM transactions WHERE user_id = ? ORDER BY timestamp DESC", session["user_id"])

    return render_template("history.html", transactions=transactions)


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
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

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

    if request.method == "POST":
        symbol = request.form.get("symbol")
        if not symbol:
            return apology("must provide symbol")

        search = lookup(symbol)
        if not bool(search):
            return apology("invalid symbol")

        return render_template("quoted.html", symbol=search["symbol"], name=search["name"], price=usd(search["price"]))

    return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    if request.method == "POST":
        # Check if user's input is blank
        username = request.form.get("username")
        if not username:
            return apology("must provide username")

        rows = db.execute("SELECT * FROM users WHERE username = ?", username)
        if len(rows) == 1:
            return apology("username already exists")

        password = request.form.get("password")
        confirmation = request.form.get("confirmation")
        if not password or not confirmation:
            return apology("must provide password")

        if password != confirmation:
            return apology("passwords doesn't match")

        hash = generate_password_hash(password)

        db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", username, hash)
        flash("Registered!")

    return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""

    if request.method == "POST":
        symbol = request.form.get("symbol")

        if not symbol:
            return apology("must provide symbol")

        shares = request.form.get("shares")
        if not shares.isnumeric() or int(shares) == 0:
            return apology("shares must be a positive integer")

        total = db.execute("SELECT SUM(shares) AS total FROM transactions WHERE user_id = ? AND symbol = ?",
                           session["user_id"], symbol)
        if db.execute("SELECT COUNT(*) AS n FROM transactions WHERE user_id = ? AND symbol = ?", session["user_id"], symbol)[0]["n"] == 0:
            return apology("invalid symbol")

        total = total[0]["total"]
        if int(shares) > total:
            return apology("too many shares")

        search = lookup(symbol)
        total = int(shares) * search["price"]
        current_cash = db.execute("SELECT * FROM users WHERE id = ?", session["user_id"])[0]["cash"]
        current_cash += total

        db.execute("INSERT INTO transactions (user_id, symbol, name, shares, price) VALUES (?, ?, ?, ?, ?)",
                   session["user_id"], symbol, search["name"], - int(shares), search["price"])
        db.execute("UPDATE users SET cash = ? WHERE id = ?", current_cash, session["user_id"])

        flash("Sold!")
        return redirect("/")

    symbols = db.execute("\
                         SELECT symbol FROM (SELECT symbol, SUM(shares) AS total FROM transactions WHERE user_id = ? GROUP BY symbol) WHERE total != 0", session["user_id"])

    return render_template("sell.html", symbols=symbols)


@app.route("/set", methods=["GET", "POST"])
@login_required
def set():
    """ Set user cash """

    if request.method == "POST":
        cash = request.form.get("cash")

        db.execute("UPDATE users SET cash = ? WHERE id = ?", cash, session["user_id"])

        flash("Cash set!")
        redirect("/")

    cash = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])[0]["cash"]

    return render_template("set.html", cash=usd(cash))

