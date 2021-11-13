"""
app.main views: render web pages with GET POST operations
Reference: O'Reilly Flask Web Development
"""

from flask import render_template, session, redirect, url_for, flash
from wtforms.validators import DataRequired
from . import main
from .. import db
from ..models import Animal
from .forms import AnimalForm, NewsForm
from datetime import datetime


def add_animals_starter():
    '''
    Insert a few animals in the Animal table as starter data
    '''
    # delete all current data
    try:
        num_rows_deleted = db.session.query(Animal).delete()
    except:
        db.session.rollback()
    starter_animals = [
        Animal(name='Kevin', type='Dog', breeds='Bulldog', good_with_animal=True, good_with_kid=True, leash_required=False, availability="Available", description="Kevin is a lovely paw patrol", data_created= datetime(2021, 11, 2, 20, 31, 10)),
        Animal(name='Snow', type='Cat', breeds='Persian', good_with_animal=True, good_with_kid=False, leash_required=False, availability="Adopted", description="Beautiful Snow loves to keep everthing quiet", data_created= datetime(2021, 10, 30, 10, 8, 1)),
        Animal(name='Tiger', type='Cat', breeds='American Shorthair', good_with_animal=True, good_with_kid=False, leash_required=False, availability="Not Available'", description="Tiger thinks of himeself as Lion King.", data_created= datetime(2021, 8, 2, 22, 10, 0)), 
        Animal(name='Charlie', type='Dog', breeds='Corgi', good_with_animal=False, good_with_kid=True, leash_required=True, availability="Pending", description="Chalie is too little to know about herself yet. She needs a warm home", data_created= datetime(2021, 6, 15, 23, 22, 5)), 
        Animal(name='Mandarin', type='Cat', breeds='American Curl', good_with_animal=True, good_with_kid=True, leash_required=False, availability="Available", description="Orange is the new color trend.", data_created= datetime(2021, 10, 15, 19, 8, 9)), 
        Animal(name='Max', type='Dog', breeds='Dalmatinac', good_with_animal=False, good_with_kid=True, leash_required=True, availability="Pending", description="Max loves to play frisbee.", data_created= datetime(2021, 12, 12, 7, 8, 11))   
    ]
    db.session.add_all(starter_animals)
    db.session.commit()

@main.route('/', methods=['GET', 'POST'])
def index():
    # order_by(Animal.data_created.desc())
    add_animals_starter()
    new_animals = Animal.query.order_by(Animal.data_created.desc()).limit(6).all()
    return render_template('index.html', new_animals=new_animals)


@main.route('/about')
def about():
    return render_template("about.html")


@main.route('/animal')
def animal():
    return render_template("animal.html")

@main.route('/contact')
def contact():
    return render_template("contact.html")

@main.route('/admin', methods=['GET', 'POST'])
def admin():
    form = AnimalForm()
    if form.validate_on_submit():
        animal = Animal(name=form.animal_name.data, 
                        type=dict(form.animal_type.choices).get(form.animal_type.data),
                        breeds=dict(form.breeds.choices).get(form.breeds.data),
                        good_with_animal=form.good_with_animal.data,
                        good_with_kid=form.good_with_kid.data,
                        leash_required=form.leash_required.data,
                        availability=dict(form.avail.choices).get(form.avail.data),
                        description=form.description.data)
        db.session.add(animal)
        db.session.commit()
        flash('New animal profile successfully created!')
        return redirect(url_for('main.index'))
    return render_template('admin.html', form=form)

@main.route('/news_item')
def news_item():
    form = NewsForm()
    return render_template("news_item.html", form=form)


