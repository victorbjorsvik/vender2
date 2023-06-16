import os
import csv
import MySQLdb

from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash


from helpers import apology, login_required

# Configure application
app = Flask(__name__)
app.run(debug=True)


# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure MySQL database
host = 'victorbjorsvik.mysql.pythonanywhere-services.com'
user = 'victorbjorsvik'
password = 'fYL24jJd4XB#hXA'
db = 'victorbjorsvik$vender'

conn = MySQLdb.Connection(db="Vender_DB.sql")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
def index():
    """Show portfolio of stocks"""


    return render_template("index.html")


@app.route("/leverandorer")
def leverandorer():

    # Create dict from database
    conn.query("""SELECT * FROM leverandorer ORDER BY telefon""")
    levs = conn.store_result()

    return render_template("leverandorer.html", levs=levs)


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
        rows = db.query("""SELECT * FROM users WHERE username = ?""", request.form.get("username"))

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



@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 400)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 400)

        if request.form.get("confirmation") != request.form.get("password"):
            return apology("Passwords must match", 400)

        # Query database for usernames
        usernames = db.query("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # username already exsists
        if len(usernames) != 0:
            return apology("Username already taken", 400)

        # Insert new user into database
        username = request.form.get("username")
        password = request.form.get("password")
        special = ['$', '@', '#', '!', '?', '*', '^', '=', '.', ',']

        # Password validation##https://stackoverflow.com/questions/41117733/validation-of-a-password-python
        if len(password) < 8:
            return apology("password must be at least 8 characters", 403)
        if len(password) > 20:
            return apology("password must be less than 20 character", 403)
        if not any(char.isdigit() for char in password):
            return apology("password must contain at least one digit", 403)
        if not any(char.isupper() for char in password):
            return apology("password must contain at least one uppercase letter", 403)
        if not any(char.islower() for char in password):
            return apology("password must contain at least one lowercase letter", 403)
        if not any(char in special for char in password):
            return apology("password must contain at least one special symbol", 403)

        # Hash password and insert into DB
        hash = generate_password_hash(password)
        db.query("INSERT INTO users (username, hash) VALUES (?, ?)", username, hash)

        return redirect("/login")

    # When requested via GET -> display registration form
    else:
        return render_template("register.html")


@app.route("/kontakt")
def kontakt():

    # Create dict from database
    contacts = db.query("SELECT * FROM kontakt")

    return render_template("kontakt.html", contacts=contacts)


@app.route("/redegjorelse")
def redegjorelse():
    return render_template("redegjorelse.html")


@app.route("/rediger_leverandorer")
@login_required
def rediger_leverandorer():
    """Legg til leverandorer i databasen"""
    leverandorer = db.query("SELECT * FROM leverandorer ORDER BY navn")

    return render_template("rediger_leverandorer.html", levs = leverandorer)

@app.route("/leggtil_leverandor", methods=["POST"])
@login_required
def leggtil_leverandor():
    """Legg til kontakter i databasen"""
    # Insert new supplier into database
    db.query("INSERT INTO leverandorer (navn, orgnummer, telefon, epost, adresse, postnummer, poststed) VALUES (?, ?, ?, ?, ?, ?, ?)",
                   request.form.get("navn"), request.form.get("orgnummer"), request.form.get("telefon"), request.form.get("epost"), request.form.get("adresse"), request.form.get("postnummer"), request.form.get("poststed"))
    flash(request.form.get("navn") + " ble lagt til", 'alert alert-success mb-0 text-center')

    return redirect("rediger_leverandorer")


@app.route("/slett_leverandor", methods=["POST"])
@login_required
def slett_leverandor():
    """Slett kontakter fra databasen"""
    # Delete current contact from DB

    db.query("DELETE FROM leverandorer WHERE navn = ?", request.form.get("navn2"))
    flash(request.form.get("navn2") + " ble fjernet", 'alert alert-danger mb-0 text-center')

    return redirect("rediger_leverandorer")


@app.route("/rediger_kontakter")
@login_required
def rediger_kontakter():
    """Legg til kontakter i databasen"""

    contacts = db.query("SELECT * FROM kontakt")

    return render_template("rediger_kontakter.html", contacts=contacts)

@app.route("/leggtil_kontakt", methods=["POST"])
@login_required
def leggtil_kontakt():
    """Legg til kontakter i databasen"""

    # Insert new supplier into database
    db.query("INSERT INTO kontakt (stilling, navn, telefon, epost) VALUES (?, ?, ?, ?)",
                request.form.get("stilling"), request.form.get("navn"), request.form.get("telefon"), request.form.get("epost"))
    flash(request.form.get("navn") + " ble lagt til", 'alert alert-success mb-0 text-center')
    return redirect("rediger_kontakter")


@app.route("/slett_kontakt", methods=["POST"])
@login_required
def slett_kontakt():
    """Slett kontakter fra databasen"""

    # Delete current contact from DB
    db.query("DELETE FROM kontakt WHERE navn = ?", request.form.get("navn2"))
    flash(request.form.get("navn2") + " ble fjernet", 'alert alert-danger mb-0 text-center')

    return redirect("rediger_kontakter")






