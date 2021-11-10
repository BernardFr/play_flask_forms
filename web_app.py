#!/usr/bin/env python

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
# import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret_key_imported_from_environment'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# FYI: leave the routes import here
from routes import *

db = SQLAlchemy(app)
# Instantiate the DB schema
# db.create_all()

if __name__ == "__main__":
    app.run(debug=True)
