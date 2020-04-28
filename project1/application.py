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
from sqlalchemy import exc, or_


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
		xyz = Book.query.all()
		return render_template("home.html", xyz=xyz, flag1=1)

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

