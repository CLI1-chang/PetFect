"""
app.main views: render web pages with GET POST operations
Reference: O'Reilly Flask Web Development
"""

from flask import render_template, session, redirect, url_for, flash, jsonify
from wtforms.validators import DataRequired
from . import main
from .. import db
from ..models import Animal
from .forms import AnimalForm, NewsForm, animal_list

@main.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


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
    form.breeds.choices = animal_list.get("Cats")
    a_type = form.animal_type.data
    a_breed = form.breeds.data

    with_animal=form.good_with_animal.data
    with_kid=form.good_with_kid.data
    leashed=form.leash_required.data

    if a_type and a_breed:
        if with_animal or with_kid or leashed:
            animal = Animal(name=form.animal_name.data, 
                            type=form.animal_type.data,
                            breeds=form.breeds.data,
                            good_with_animal=form.good_with_animal.data,
                            good_with_kid=form.good_with_kid.data,
                            leash_required=form.leash_required.data,
                            availability=dict(form.avail.choices).get(form.avail.data),
                            description=form.description.data)
            db.session.add(animal)
            db.session.commit()
            flash('New animal profile successfully created!')
            return redirect(url_for('main.index'))
        else:
            # needs to add in an alert of somesort
            print('Please choose a Disposition')
    else:
        print(form.errors)
    return render_template('admin.html', form=form)

@main.route('/animal_breed/<type>')
def animal_breed(type):
    breeds = animal_list.get(type)
    print (breeds)
    return jsonify({'breeds': breeds})

@main.route('/news_item')
def news_item():
    form = NewsForm()
    return render_template("news_item.html", form=form)


