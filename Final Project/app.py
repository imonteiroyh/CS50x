import os
import json

from cs50 import SQL
from flask import Flask, redirect, render_template, request, session, flash
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import search_omdb, get_total_seasons_omdb, login_required

app = Flask(__name__)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config["SESSION_COOKIE_SAMESITE"] = 'Strict'
Session(app)

if 'tracker.db' not in os.listdir():
    try:
        open('tracker.db', mode='a').close()
    except OSError:
        print('Failed creating tracker.db')

db = SQL("sqlite:///tracker.db")

if not len(db.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users'")):
    db.execute("CREATE TABLE users (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, username TEXT NOT NULL, hash TEXT NOT NULL)")
    db.execute("CREATE UNIQUE INDEX username ON users (username)")

if not len(db.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='media'")):
    db.execute("CREATE TABLE media (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, user_id INTEGER NOT NULL, imdbID TEXT NOT NULL, title TEXT NOT NULL, status TEXT NOT NULL DEFAULT 'Plan to Watch', media_type TEXT NOT NULL, poster TEXT NOT NULL, user_season INTEGER, total_seasons INTEGER, timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)")


@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidade"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":
        username = request.form.get("username")
        if not username:
            flash("Must provide a username!")
            return render_template("register.html")

        rows = db.execute("SELECT * FROM users WHERE username = ?", username)
        if len(rows) == 1:
            flash("Username already in use!")
            return render_template("register.html")

        password = request.form.get("password")
        if not password:
            flash("Must provide a password!")
            return render_template("register.html")

        confirmation = request.form.get("confirmation")
        if not confirmation:
            flash("Must provide the password confirmation!")
            return render_template("register.html")

        if password != confirmation:
            flash("Passwords does not match!")
            return render_template("register.html")

        hash = generate_password_hash(password)

        db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", username, hash)
        flash("Registered!")
        return redirect("/login")


    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    session.clear()

    if request.method == "POST":
        username = request.form.get("username")
        if not username:
            flash("Must provide a username!")
            return render_template("login.html")

        password = request.form.get("password")
        if not password:
            flash("Must provide a password!")
            return render_template("login.html")

        rows = db.execute("SELECT * FROM users WHERE username = ?", username)
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], password):
            flash("Invalid username and/or password!")
            return render_template("login.html")

        session["user_id"] = rows[0]["id"]

        return redirect("/")

    return render_template("login.html")


@app.route("/logout")
def logout():

    session.clear()
    return redirect("/login")


@app.route("/")
@login_required
def index():

    movies = db.execute("SELECT imdbID, title, status, poster, media_type FROM media WHERE media_type = 'Movie' AND user_id = ?", session["user_id"])
    series = db.execute("SELECT imdbID, title, status, poster, media_type, user_season, total_seasons FROM media WHERE media_type = 'Series' AND user_id = ?", session["user_id"])

    return render_template("index.html", movies=movies, series=series)


@app.route("/search", methods=["GET", "POST"])
@login_required
def search():

    if request.method == "POST":
        title = request.form.get("title")

        if not title:
            flash("Must provide a title!")
            return redirect("/")

        results = search_omdb(title)
        if not results:
            flash("Results not found!")
            return redirect("/")

        for result in results.copy():
            result["Type"] = result["Type"].capitalize()
            if result["Type"] not in ['Movie', 'Series']:
                results.remove(result)

        return render_template("search.html", medias=results)

    return redirect("/")


@app.route("/add_media", methods=["GET", "POST"])
@login_required
def add_media():

    if request.method == "POST":
        medias = request.form.getlist("select-media")

        if not medias:
            flash('Media not selected!')
            return redirect("/")

        for media in medias:
            media = json.loads(media.replace("\'", "\""))

            if media["Type"] == 'Movie':
                db.execute("INSERT INTO media (user_id, imdbID, title, media_type, poster) VALUES (?, ?, ?, ?, ?)", session["user_id"], media["imdbID"], media["Title"], media["Type"], media["Poster"])
            else:
                total_seasons = get_total_seasons_omdb(media["imdbID"])
                db.execute("INSERT INTO media (user_id, imdbID, title, media_type, poster, user_season, total_seasons) VALUES (?, ?, ?, ?, ?, ?, ?)", session["user_id"], media["imdbID"], media["Title"], media["Type"], media["Poster"], 1, total_seasons)

        flash('Media succesfully added!')

    return redirect("/")

@app.route("/remove_media", methods=["GET", "POST"])
@login_required
def remove_media():

    if request.method == "POST":
        medias = request.get_json()

        if not medias:
            return redirect("/")

        for media in medias:
            media = json.loads(media.replace("\'", "\""))
            db.execute("DELETE FROM media WHERE user_id = ? AND imdbID = ?", session["user_id"], media["imdbID"])

        return redirect("/")

    return redirect("/")


@app.route("/reset_media", methods=["GET", "POST"])
@login_required
def reset_media():

    if request.method == "POST":
        medias = request.get_json()

        if not medias:
            return redirect("/")

        for media in medias:
            media = json.loads(media.replace("\'", "\""))

            if media["media_type"] == "Series":
                db.execute("UPDATE media SET user_season = ? WHERE user_id = ? AND imdbID = ?", 1, session["user_id"], media["imdbID"])

        return redirect("/")

    return redirect("/")


@app.route("/increment_season", methods=["POST"])
@login_required
def increment_season():

    imdbID = request.get_json()["id"]
    season = request.get_json()["season"]
    db.execute("UPDATE media SET user_season = ? WHERE user_id = ? AND imdbID = ?", season, session["user_id"], imdbID)

    return redirect("/")


@app.route("/update_status", methods=["POST"])
@login_required
def update_status():

    imdbID = request.get_json()["id"]
    status = request.get_json()["status"]
    db.execute("UPDATE media SET status = ? WHERE user_id = ? AND imdbID = ?", status, session["user_id"], imdbID)

    return redirect("/")