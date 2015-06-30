from flask import render_template, url_for, redirect, flash, request

from hoopsapp import app, db
from hoopsapp.models import Teams, Players
from hoopsapp.forms import TeamForm
import urlparse


@app.route('/', methods=['GET', 'POST'])
def index():


    teams = Teams.query.all()   
    flash("Please select Team 1")
    return render_template('index.html', teams=teams)




def static(path):
    root = app.config.get('STATIC_ROOT')
    if root is None:
        return url_for('static', filename=path)
    else:
        return urlparse.urljoin(root, path)

@app.context_processor
def context_processor():
    return dict(static=static)