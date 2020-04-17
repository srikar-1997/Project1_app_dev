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
os.environ["DATABASE_URL"] = "postgres://vdsjxpbuoklrgr:1669a5d62c3c6e5aaf3c580c4245a3703c760912beb63a870d62f93c69e6b45f@ec2-54-88-130-244.compute-1.amazonaws.com:5432/d8ijt27ijeed12"
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

# # Check for environment variable
# if not os.getenv("DATABASE_URL"):
#     raise RuntimeError("DATABASE_URL is not set")

# # Configure session to use filesystem
# app.config["SESSION_PERMANENT"] = False
# app.config["SESSION_TYPE"] = "filesystem"
# Session(app)

# # Set up database
# engine = create_engine(os.getenv("DATABASE_URL"))
# db = scoped_session(sessionmaker(bind=engine))


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

        # reg = Users(username = name, password = pwd, timestamp = time_stamp)
        # # reg1 = Users.query.get(reg.username)
        # db.session.add(reg)
        # db.session.commit()
        # return render_template("success.html")
        reg = Users(username = name, password = hashed, timestamp = time_stamp)
        try:
            reg1 = Users.query.get(reg.username)
            db.session.add(reg)
            db.session.commit()
            return render_template("success.html")
        # except exc.IntegrityError:
        #     return render_template("userexist.html")
        except:
            logging.debug('exception message', 'something went wrong in adding user')
    return render_template("userexist.html")
        
@app.route("/admin")
def admin():
    users = Users.query.order_by(Users.timestamp).all()
    return render_template("users.html", users = users)

