import os
import datetime
import bcrypt
from models import *

from flask import Flask, session, render_template, request, redirect, url_for, jsonify
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
import logging
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import exc, or_, and_


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
        # xyz = Book.query.all()
        # return render_template("home.html", xyz=xyz, flag1=1)
        return render_template("newhome.html")

@app.route("/search", methods = ["POST"])
def search():
        if request.method == 'POST':
            key = request.form.get('search2')
            key = key.title()
            key = "%"+key+"%"
            search_list = []
            filtered_list1 = Book.query.filter(or_(Book.ISBN.like(key), Book.year.like(key), Book.author.like(key), Book.title.like(key))).all()
            if filtered_list1:
                search_list.append(2)
                if isinstance(filtered_list1, list):
                    return render_template("home.html", filtered_list=filtered_list1, flag3=1)
                else:
                    return render_template("home.html", filtered_list=filtered_list1, flag2=1)


            if not search_list:
                return render_template("home.html", filtered_list=filtered_list1, flag4=1)
                
    

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
        if userobj:
            if pwd == userobj.password :
                session["name"] = name
                return redirect(url_for('index'))
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
        Book_obj = Book.query.get(ISBN)
        isb = Review.query.filter_by(ISBN_No = ISBN).all()
        rev = Review.query.filter(and_(Review.name == name, Review.ISBN_No == ISBN)).first()
        if rev and rev.review_rate is not None and rev.review_description is not None :
            if isb == []:
                return render_template("bookpage.html", sub_flag = 1, isb_flag = 0, Bookobject = Book_obj)
            else:
                return render_template("bookpage.html", sub_flag = 1, isb = isb, isb_flag = 1, Bookobject = Book_obj)
        else :
            if isb == []:
                return render_template("bookpage.html", ISBN = ISBN, isb_flag = 0, Bookobject = Book_obj)
            else :
                return render_template("bookpage.html", isb = isb, ISBN = ISBN, isb_flag = 1, Bookobject = Book_obj)

    

@app.route("/review/<ISBN>", methods = ["POST"])
def review(ISBN):
    name = session["name"]
    # ISBN = "1416949658"
    isb = Review.query.filter_by(ISBN_No = ISBN).all()
    rev = Review.query.filter(and_(Review.name == name, Review.ISBN_No == ISBN)).first()
    #if request.form['action'] != "comment":
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
        return redirect(url_for('book_details', ISBN = ISBN))
    if request.form['action'] == "comment":
        rev.review_description = request.form.get("text")
        db.session.commit()
                # return render_template("bookpage.html", flag = 1, sub_flag_1 = 1)
        return redirect(url_for('book_details', ISBN = ISBN))

    return redirect(url_for('book_details', ISBN = ISBN))

@app.route("/api/submit_review", methods = ["POST"])
def review_api():
    data = request.get_json()
    name = session["name"]
    ISBN = request.form.get('ISBN')
    rate = request.form.get('rate')
    comment = request.form.get("comment")
    revi = Review.query.filter(and_(Review.name == name, Review.ISBN_No == ISBN)).first()
    if  revi is None:
        rev = Review(name = name, ISBN_No = ISBN, review_rate = rate, review_description = comment)
        db.session.add(rev)
        db.session.commit()
        return jsonify({"success": True, "rate" : rate, "comment" : comment, "status":"200"})
    elif revi and revi.review_rate is not None and revi.review_description is not None :
        revi.review_description = comment
        revi.review_rate = rate
        db.session.add(revi)
        db.session.commit()
        return jsonify({"success": True, "rate" : rate, "comment" : comment, "status":"200"})
    else:
        return jsonify({"success": False})


@app.route("/api/search", methods = ["POST", "GET"])
def search_api():
    data = request.get_json()
    key = request.form.get('key')
    # key = data["key"]
    key = key.title()
    key = "%"+key+"%"
    dbooks = {"books":[]}
    filtered_list1 = Book.query.filter(or_(Book.ISBN.like(key), Book.year.like(key), Book.author.like(key), Book.title.like(key))).all()
    if filtered_list1:
        if isinstance(filtered_list1, list):
            for i in filtered_list1:
                dic = dict()
                dic["ISBN"] = i.ISBN
                dic["Title"] = i.title
                dic["Author"] = i.author
                dic["Year"] = i.year
                dbooks["books"].append(dic)
            dbooks["success"] = True
            return jsonify(dbooks)
                
        else :
            return jsonify({"ISBN": filtered_list1.ISBN,"Title": filtered_list1.title, "Author": filtered_list1.author, "year": filtered_list1.year})
    
    return jsonify({"error": "No Books"}), 400

@app.route("/api/bookpage", methods = ["POST", "GET"])
def bookpage_api():
    data = request.get_json()
    ISBN = request.form.get('ISBN')
    Book_obj = Book.query.get(ISBN)
    isb = Review.query.filter_by(ISBN_No = ISBN).all()
    revs = []

    if isb == []:
        return jsonify({"success": True, "ISBN" : Book_obj.ISBN, "Title" : Book_obj.title, "Author": Book_obj.author, "Year" : Book_obj.year})
    else :
        for i in isb:
            dic = dict()
            dic["Name"] = i.name
            dic["rate"] = i.review_rate
            dic["comm"] = i.review_description
            revs.append(dic)
        return jsonify({"success": True, "ISBN" : Book_obj.ISBN, "Title" : Book_obj.title, "Author": Book_obj.author, "Year" : Book_obj.year, "revs" : revs})
