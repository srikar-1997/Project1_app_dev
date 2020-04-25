import os
import datetime
import bcrypt
from models import *

from flask import Flask, session, render_template, request, redirect, url_for
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
import logging
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import exc, and_, text


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


@app.route("/")
def index():
    if 'name' not in session :
        return redirect(url_for('register'))
    elif session['name'] :
        return render_template("home.html")
    

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for('register'))

@app.route("/register", methods = ["GET", "POST"] )
def register():
    if request.method == "GET":
        return render_template("Registration.html")
    elif request.form['action'] == 'register':
        flag = 0
        name = request.form.get("username")
        pwd = request.form.get("password")
        time_stamp = datetime.datetime.now()
        reg = Users(username = name, password = pwd, timestamp = time_stamp)
        try:
            
            db.session.add(reg)
            db.session.commit()
            return render_template("Registration.html", flag_3 = 1)
        except exc.IntegrityError:
            flag = 1
            return render_template("Registration.html", flag = flag)
            # return render_template("userexist.html")
        except:
            print('exception message', 'something went wrong in adding user')
    elif request.form['action'] == 'login':
        authentication()

@app.route("/auth", methods = ["GET", "POST"])
def authentication():
    if request.method == "POST":
        name = request.form.get("username")
        pwd = request.form.get("password")
        userobj = Users.query.get(name)
        # print(Users.query.get("xyz"))
        if userobj:
            if pwd == userobj.password :
                session["name"] = name
                return redirect(url_for('index'))
                # return redirect(url_for('index'))
                # if session.get('name') is None:
            else :
                return render_template("Registration.html", flag_1= 1)
        else :
            return render_template("Registration.html", flag_2 = 1)

    
@app.route("/admin")
def admin():
    users = Users.query.order_by(Users.timestamp).all()
    return render_template("users.html", users = users)

@app.route("/book/<ISBN>", methods = ["GET"])
def book_details(ISBN):
    name = session["name"]
    # ISBN = "1416949658"
    if request.method == "GET":
        isb = Review.query.filter_by(ISBN_No = ISBN).all()
        rev = Review.query.filter(and_(Review.name == name, Review.ISBN_No == ISBN)).first()
        if rev and rev.review_rate is not None and rev.review_description is not None :
            return render_template("submit.html", sub_flag = 1, rate = rev.review_rate, comm = rev.review_description, isb = isb)
        return render_template("submit.html", isb = isb, ISBN = ISBN)

    

@app.route("/book/<ISBN>", methods = ["POST"])
def review(ISBN):
    name = session["name"]
    # ISBN = "1416949658"
    isb = Review.query.filter_by(ISBN_No = ISBN).all()
    rev = Review.query.filter(and_(Review.name == name, Review.ISBN_No == ISBN)).first()
    if request.form['action'] != "comment":
        if rev is None:
            rev = Review(name = name, ISBN_No = ISBN, review_rate = None, review_description = None)
            db.session.add(rev)
        if request.form['action'] == "1":
            rev.review_rate = 1
        elif request.form['action'] == "2":
            rev.review_rate = 2
        elif request.form['action'] == "3":
            rev.review_rate = 3
        elif request.form['action'] == "4":
            rev.review_rate = 4
        elif request.form['action'] == "5":
            rev.review_rate = 5
        db.session.commit()
        return render_template("submit.html", isb = isb, ISBN = ISBN)
    if request.form['action'] == "comment":
        rev.review_description = request.form.get("text")
        db.session.commit()
                # return render_template("submit.html", flag = 1, sub_flag_1 = 1)
        return redirect(url_for('review', ISBN = ISBN))

    return redirect(url_for("review", ISBN = ISBN))
        
# @app.route("submit")
# def submit:
#         db.session.add(review)
#         db.session.commit()
#         return redirect(url_for('submit'))
