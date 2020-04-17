import os

from flask import Flask, render_template, request
from models import *

app = Flask(__name__)
os.environ["DATABASE_URL"] = "postgres://vdsjxpbuoklrgr:1669a5d62c3c6e5aaf3c580c4245a3703c760912beb63a870d62f93c69e6b45f@ec2-54-88-130-244.compute-1.amazonaws.com:5432/d8ijt27ijeed12"
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

def main():
    db.create_all()

if __name__ == "__main__":
    with app.app_context():
        main()
