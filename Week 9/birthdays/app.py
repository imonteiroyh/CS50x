import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///birthdays.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":

        id = request.form.get("id")
        if id is not None:
            db.execute("DELETE FROM birthdays WHERE id = ?", id)

            return redirect("/")

        name = request.form.get("name")
        month = request.form.get("month")
        day = request.form.get("day")

        current_id = db.execute("SELECT id FROM birthdays ORDER BY id DESC LIMIT 1")
        db.execute("INSERT INTO birthdays (id, name, month, day) VALUES (?, ?, ?, ?)", current_id[0]["id"] + 1, name, month, day)


        return redirect("/")

    else:

        birthdays = db.execute("SELECT * FROM birthdays")

        return render_template("index.html", birthdays=birthdays)


