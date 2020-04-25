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

class Review(db.Model) :
    __tablename__ = "reviews"

    __table_args__ = (db.PrimaryKeyConstraint('name', 'ISBN_No'),)
    name = db.Column(db.String, db.ForeignKey('users.username'))
    ISBN_No = db.Column(db.String, db.ForeignKey('books.ISBN'))
    review_rate = db.Column(db.Integer)
    review_description = db.Column(db.String)

    def __init__ (self, name, ISBN_No, review_rate, review_description) :
        self.name = name
        self.ISBN_No = ISBN_No
        self.review_rate = review_rate
        self.review_description = review_description