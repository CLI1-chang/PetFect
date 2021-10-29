from flask import render_template, session, redirect, url_for, flash
from wtforms.validators import DataRequired
from . import main
from .. import db
from ..models import Animal
from .forms import AnimalForm


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
        animal = Animal(name=form.animal_name.data, 
                        type=form.animal_type.data,
                        breeds=form.breeds.data,
                        good_with_animal=form.good_with_animal.data,
                        good_with_kid=form.good_with_kid.data,
                        leash_required=form.leash_required.data,
                        availability=form.avail.data,
                        description=form.description.data)
        db.session.add(animal)
        db.session.commit()
        flash('New animal profile successfully created!')
        return redirect(url_for('main.index'))
    return render_template('admin.html', form=form)

@main.route('/contact')
def contact():
    return render_template("contact.html")

