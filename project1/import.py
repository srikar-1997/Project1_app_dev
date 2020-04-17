import csv
import os

from flask import Flask, render_template, request
from models import *

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

def main():
    f = open("books.csv")
    reader = csv.reader(f)
    for ISBN, title, author, pubyear in reader:
        book = Book(ISBN = ISBN, title = title, author = author, year = pubyear)
        db.session.add(book)
        # print(f"Added book with ISBN no {ISBN} of title {title} written by author {author} published in the year {pubyear}")
    db.session.commit()

if __name__ == "__main__":
    with app.app_context():
        main()