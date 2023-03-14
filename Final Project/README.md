# MyMedia Tracker
#### Description:
MyMedia Tracker is a web application that allows users to keep track of the movies and TV shows they watch. Users can register an account, log in and add media to their account. For TV shows, users can track the season they are currently watching and update the status of the media as they watch it.

The application uses the OMDb API to search for movies and TV shows by title and imdbID and allows users to add or remove the media to their account from the search results. The application is built using Python, Javascript, HTML and CSS, Flask and Bootstrap frameworks was also used. The application uses a SQLite database to store user account information and media data.

The files used in the project are:

script.js: Script that handles selection of tables to be displayed, removal of media from table, resetting of series' seasons, incrementing of watched seasons and selection of media status.

styles.css: Defines font for the title, navigation bar and adjusts for the mobile version of the site.

index.html: Main page where users can select whether to view added movies or added TV shows and perform almost all of the application's functions.

layout.html: Standard template for HTML files.

login.html: Page for users to log in to their account.

register.html: Page for users to register a new account.

search.html: Page where interaction with the OMDb API to obtain information about movies and TV shows is displayed after the search is performed, showing the search results that are movies or series among the 10 top search results.

helpers.py: Implementation of the search function for the OMDb API, implementation of the function to find the number of seasons for a TV show according to OMDb API, creation of the decorator function for functions that require login.

requirements.txt: Requirements for the project.

token.txt: Token for the OMDb API used in the project.

tracker.db: Automatically created by app.py, containing the users table with (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, username TEXT NOT NULL, hash TEXT NOT NULL) and the media table with (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, user_id INTEGER NOT NULL, imdbID TEXT NOT NULL, title TEXT NOT NULL, status TEXT NOT NULL DEFAULT 'Plan to Watch', media_type TEXT NOT NULL, poster TEXT NOT NULL, user_season INTEGER, total_seasons INTEGER, timestamp DATETIME DEFAULT CURRENT_TIMESTAMP).

app.py: Script that creates the tracker.db file and its tables, configures the session with Flask and has the functionalities represented by the following routes: "/register", "/login", "/logout", "/index", "/search", "/add_media", "/remove_media", "/reset_media", "/increment_season", "/update_status" with which the interaction with the database is done when necessary (using SQL with the CS50 library).

The functions of the application can be summarized below:

    register: This function implements the register functionality. The function handles GET and POST requests to the "/register" route. When a POST request is received, the function first checks if the informations of username, password and password confirmation provided are valid and renders the "register.html" template if not. If the passwords match, the function generates a password hash using the generate_password_hash() function from the Werkzeug security module. The username and password hash are then inserted into the "users" table in the database using the db.execute() function. Finally, the function flashes a message indicating that the user has been registered and redirects the user to the "/login" URL. In the GET request, the function simply renders the "register.html" template. One design choice made in this function is to use the Flask flash function to display error messages to the user if they provide invalid information or not provide it. This provides immediate feedback to the user and improves the user experience.

    login: This function implements the login functionality. The function handles GET and POST requests to the "/login" route. When a POST request is received, it retrieves the username and password from the form data. It then checks if the username exists in the database and if the password provided matches the hashed password stored in the database. If the username and password combination is correct, it sets the user_id in the session and redirects the user to the homepage ("/"). The function also clears the session when a GET request is received. This is a good security practice to ensure that any existing session information is removed before a new user logs in. One design choice made in this function is to use the Flask flash function to display error messages to the user if they provide invalid login information. This provides immediate feedback to the user and improves the user experience.

    logout: This function implements the log out functionality. When the user accesses this route, it clears the session data and redirects the user to the login page. This design choice is to ensure that the user's session data is deleted from the server, preventing unauthorized access to the user's account.

    index: This function is a route for the homepage. The function queries the database to retrieve the movies and TV series that belong to the currently logged-in user and then renders the index.html template, passing the retrieved movies and series as arguments to the template. The @login_required decorator is added to restrict access to the page only to authenticated users.

    search: This function implements the search functionality of the application. The function handles GET and POST requests to the "/search" route. This function use is to search for movies and series using the Open Movie Database (OMDb) API. The function first checks if a POST request has been made and if so, it extracts the title from the form data. If the title is not provided, it displays a flash message and redirects to the index page. If the title is provided, the function uses the search_omdb function to retrieve search results from the OMDb API. If no results are found, a flash message is displayed and the function redirects to the index page. If results are found, the function modifies each result to capitalize the media type (i.e. "movie" becomes "Movie") and removes any results that are not either movies or series. The function renders the search.html template with the search results. The @login_required decorator is added to restrict access to the page only to authenticated users. The function also uses flash messages to provide immediate feedback to the user.

    add_media: This function implements the addition of media to a user's list functionality. The function handles GET and POST requests to the "/add_media" route. When a GET request is received, the user is redirected to "/". The user can select one or more movies or TV shows from the search results and add them to their media list. When the user selects media to add, the function receives a list of selected media and iterates over it. For each TV show, the function retrieves the number of total seasons from the OBDB API. The @login_required decorator is added to restrict access to the page only to authenticated users. The function also uses flash messages to provide immediate feedback to the user.

    remove_media: This function implements the removing of media from a user's list functionality. The function handles GET and POST requests to the "/remove_media" route. When a GET request is received, the user is redirected to "/". The user can select one or more movies or TV shows from the user's list and select a button to remove them from their media list. When the user selects media to remove, the function receives a list of selected media and iterates over it deleting from the media table. The @login_required decorator is added to restrict access to the page only to authenticated users. This functionality also uses javascript script to set the row of the selected medias' display to none, providing immediate feedback to the user.

    reset_media: This function implements the resetting of seasons of series media from user's list functionality. The function handles GET and POST requests to the "/reset_media" route. When a GET request is received, the user is redirected to "/". Like the remove_media function, the user can select one or more movies or series from the user's list and select a button to reset their seasons. The function receives a list of select media and interates over it ignoring movies and updating the user_season value of the media table to 1. The @login_required decorator is added to restrict access to the page only to authenticated users. This functionality also uses a javascript script to set the value of the season the user is in immediatly to 1, providing immediate feedback to the user.

    increment_season: This function is used to increment the season of a specific series of the user's list. The function receives a json file exported with the use of a javascript script with informations about the imdbID and the season that the series have to be set. The @login_required decorator is added to restrict access to the page only to authenticated users. This functionality also uses a javascript script to set the value of the season the user is in immediatly, providing immediate feedback to the user.

    update_status: This function is used to update the status of a specific movie or series of the user's list. The function receives a json file exported with the use of a javascript script with informations about the imdbID and the status that the movie or series have to be set. Jinja was used to set and get the value of the select tag on index.html. The @login_required decorator is added to restrict access to the page only to authenticated users. This functionality also uses a javascript script to set the value of the season the user is in immediatly, providing immediate feedback to the user.