from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_pyfile('..\config.py')

#initialize SQLAlchemy db to work with our flask app
db = SQLAlchemy(app)

#import the MVC
import hoopsapp.models
import hoopsapp.forms

#setup the db and configure the tables
db.create_all()

import hoopsapp.views