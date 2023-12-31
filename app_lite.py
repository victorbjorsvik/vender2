import os
import csv

from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required

# Configure application
app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
def index():
    """Hjemmeside"""

    return render_template("index.html")



@app.route("/kontakt")
def kontakt():
    """OVersikt over kontaktinformasjon"""

    return render_template("kontakt.html", active='kontakt')


@app.route("/redegjorelse")
def redegjorelse():
    """Publisering av rapport iht. åpenhetsloven"""

    return render_template("redegjorelse.html", active='redegjorelse')








