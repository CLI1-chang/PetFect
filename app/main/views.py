from flask import render_template, session, redirect, url_for
from . import main
from .. import db
from ..models import User
from .forms import NameForm, AnimalForm


@main.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


@main.route('/about')
def about():
    return render_template("about.html")

@main.route('/animal')
def animal():
    return render_template("animal.html")

@main.route('/admin', methods=['GET', 'POST'])
def admin():
    form = AnimalForm()
    if form.validate_on_submit():
        return 'Form successfuly submitted!'
    return render_template('admin.html', form=form)

@main.route('/contact')
def contact():
    return render_template("contact.html")

