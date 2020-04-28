from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Users(db.Model) :
    __tablename__ = "users"
    username = db.Column(db.String, primary_key=True)
    password = db.Column(db.String, nullable=False)
    timestamp = db.Column(db.DateTime(), nullable=False)

    def __init__ (self, username, password, timestamp) :
        self.username = username
        self.password = password
        self.timestamp = timestamp

class Book(db.Model) :
    __tablename__ = "books"
    ISBN = db.Column(db.String, primary_key=True)
    title = db.Column(db.String, nullable=False)
    author = db.Column(db.String, nullable=False)
    year = db.Column(db.String, nullable=False)

    def __init__ (self, ISBN, title, author, year) :
        self.ISBN = ISBN
        self.title = title
        self.author = author
        self.year = year

