"""
app.main views: render web pages with GET POST operations
Reference: O'Reilly Flask Web Development
"""

from flask import render_template, session, redirect, url_for, flash, jsonify, request, Response
# from wtforms.validators import DataRequired
from . import main
from .. import db
from datetime import datetime
from ..models import Animal, User
from .forms import AnimalForm, NewsForm, animal_list, EditProfileForm, EditProfileAdminForm
from werkzeug.utils import secure_filename
from flask_login import login_required, current_user
from ..decorators import admin_required


def add_animals_starter():
    '''
    Insert a few animals in the Animal table as starter data
    '''
    # delete all current data
    # try:
    #     num_rows_deleted = db.session.query(Animal).delete()
    # except:
    #     db.session.rollback()
    starter_animals = [
        Animal(
            name='Kevin', type='Dog', breeds='Bulldog', good_with_animal=True, good_with_kid=True, leash_required=False, availability="Available", 
            description="Kevin is a lovely paw patrol", data_created= datetime(2021, 11, 2, 20, 31, 10),
            img = open('app/static/1_dog_kevin.jpeg', 'r'),
            img_name = "test",
            img_mimetype = "test")
        # Animal(name='Snow', type='Cat', breeds='Persian', good_with_animal=True, good_with_kid=False, leash_required=False, availability="Adopted", description="Beautiful Snow loves to keep everthing quiet", data_created= datetime(2021, 10, 30, 10, 8, 1)),
        # Animal(name='Tiger', type='Cat', breeds='American Shorthair', good_with_animal=True, good_with_kid=False, leash_required=False, availability="Not Available'", description="Tiger thinks of himeself as Lion King.", data_created= datetime(2021, 8, 2, 22, 10, 0)), 
        # Animal(name='Charlie', type='Dog', breeds='Corgi', good_with_animal=False, good_with_kid=True, leash_required=True, availability="Pending", description="Chalie is too little to know about herself yet. She needs a warm home", data_created= datetime(2021, 6, 15, 23, 22, 5)), 
        # Animal(name='Mandarin', type='Cat', breeds='American Curl', good_with_animal=True, good_with_kid=True, leash_required=False, availability="Available", description="Orange is the new color trend.", data_created= datetime(2021, 10, 15, 19, 8, 9)), 
        # Animal(name='Max', type='Dog', breeds='Dalmatinac', good_with_animal=False, good_with_kid=True, leash_required=True, availability="Pending", description="Max loves to play frisbee.", data_created= datetime(2021, 12, 12, 7, 8, 11))   
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
    form.breeds.choices = animal_list.get("Cats")
    a_type = form.animal_type.data
    a_breed = form.breeds.data

    with_animal=form.good_with_animal.data
    with_kid=form.good_with_kid.data
    leashed=form.leash_required.data
  
    if a_type and a_breed and form.image.data:
        if with_animal or with_kid or leashed:
            file = request.files[form.image.name]
            print("Breed is", a_breed)
            animal = Animal(name=form.animal_name.data, 
                            type=form.animal_type.data,
                            breeds=a_breed,
                            good_with_animal=form.good_with_animal.data,
                            good_with_kid=form.good_with_kid.data,
                            leash_required=form.leash_required.data,
                            img = file.read(),
                            img_name = secure_filename(file.filename),
                            img_mimetype = file.mimetype,
                            availability=dict(form.avail.choices).get(form.avail.data),
                            description=form.description.data)
            db.session.add(animal)
            db.session.commit()
            flash('New animal profile successfully created!')
            return redirect(url_for('main.index'))
        else:
            # needs to add in an alert 
           print('Must select a disposition!')
    return render_template('admin.html', form=form)


@main.route('/animal_breed/<type>')
def animal_breed(type):
    breeds = animal_list.get(type)
    return jsonify({'breeds': breeds})

@main.route('/news_item')
def news_item():
    form = NewsForm()
    return render_template("news_item.html", form=form)


@main.route('/user/<user_name>')
def user(user_name):
    curr_user = User.query.filter_by(user_name=user_name).first_or_404()
    return render_template('user.html', user=curr_user)


@main.route('/edit-profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.name = form.name.data
        current_user.location = form.location.data
        current_user.about_me = form.about_me.data
        db.session.add(current_user._get_current_object())
        db.session.commit()
        flash('Update your profile successfully!')
        print(current_user.user_name)
        return redirect(url_for('main.user', user_name=current_user.user_name))
    form.name.data = current_user.name
    form.location.data = current_user.location
    form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', form=form)


@main.route('/edit-profile/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_profile_admin(id):
    admin_user = User.query.get_or_404(id)
    form = EditProfileAdminForm()
    if form.validate_on_submit():
        admin_user.name = form.name.data
        admin_user.location = form.location.data
        admin_user.about_me = form.about_me.data
        db.session.add(admin_user)
        db.session.commit()
        flash('Update your profile successfully!')
        return redirect(url_for('main.user', user_name=admin_user.user_name))
    form.name.data = admin_user.name
    form.location.data = admin_user.location
    form.about_me.data = admin_user.about_me
    return render_template('edit_profile_admin.html', form=form)

