import os
import datetime
import bcrypt
from models import *

from flask import Flask, session, render_template, request
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
import logging
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import exc


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

@app.route("/")
def index():
    return "Hello"

@app.route("/register", methods = ["GET", "POST"] )
def register():
    if request.method == "GET":
        return render_template("Registration.html")
    else:
        name = request.form.get("username")
        pwd = request.form.get("password")
        pwd = pwd.encode('utf-8')
        hashed = bcrypt.hashpw(pwd, bcrypt.gensalt())
        time_stamp = datetime.datetime.now()
        reg = Users(username = name, password = hashed, timestamp = time_stamp)
        try:
            
            db.session.add(reg)
            db.session.commit()
            return render_template("success.html")
        except exc.IntegrityError:
            return render_template("userexist.html")
        except:
            print('exception message', 'something went wrong in adding user')

        
@app.route("/admin")
def admin():
    users = Users.query.order_by(Users.timestamp).all()
    return render_template("users.html", users = users)

