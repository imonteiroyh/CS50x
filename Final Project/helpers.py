import requests

from flask import redirect, session
from functools import wraps


def search_omdb(name):

    try:
        with open('token.txt') as token:
            api_key = token.read()

        url = f"http://www.omdbapi.com/?apikey={api_key}&s={name}"
        response = requests.get(url)
        response.raise_for_status()

    except requests.RequestException:
        return None

    try:
        search_results = response.json()["Search"]
        return search_results

    except (KeyError, TypeError, ValueError):
        return None

def get_total_seasons_omdb(imdbID):

    try:
        with open('token.txt') as token:
            api_key = token.read()

        url = f"http://www.omdbapi.com/?apikey={api_key}&i={imdbID}"
        response = requests.get(url)
        response.raise_for_status()

    except requests.RequestException:
        return None

    try:
        total_seasons = response.json()["totalSeasons"]
        return total_seasons

    except (KeyError, TypeError, ValueError):
        return None


def login_required(f):

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)

    return decorated_function


