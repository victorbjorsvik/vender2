import csv

from cs50 import SQL


# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

# Insert leverandorer into DB
leverandorer = []

# Import Data
with open("lev3.csv", mode="r") as database:
    file_reader = csv.DictReader(database)
    for row in file_reader:
        leverandorer.append(row)

# Insert data into DB
for i in range(len(leverandorer)):
    db.execute("INSERT INTO leverandorer (leverandornummer, navn, orgnummer, telefon, mobil, epost, adresse, postnummer, poststed, land) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ? )",
    leverandorer[i]['\ufeffLeverandørnummer'], leverandorer[i]['Navn'], leverandorer[i]['Organisasjonsnummer'], leverandorer[i]['Telefonnummer'], leverandorer[i]['Telefonnr. mobil'], leverandorer[i]['E-postadresse'],
    leverandorer[i]['Forretningsadresse Linje'], leverandorer[i]['Postadresse Postnr.'], leverandorer[i]['Postadresse Sted'], leverandorer[i]['Forretningsadresse Land'])
