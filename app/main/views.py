from flask import render_template, session, redirect, url_for
from . import main
from .. import db
from ..models import User
from .forms import NameForm


@main.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


@main.route('/about')
def about():
    return render_template("about.html")


@main.route('/animal')
def animal():
    return render_template("animal.html")
