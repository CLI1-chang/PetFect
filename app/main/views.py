"""
app.main views: render web pages with GET POST operations
Reference: O'Reilly Flask Web Development
"""

from flask import render_template, session, redirect, url_for, flash, jsonify, request, Response
# from wtforms.validators import DataRequired
from . import main
from .. import db
from ..models import Animal, User
from .forms import AnimalForm, NewsForm, animal_list, EditProfileForm, EditProfileAdminForm
from werkzeug.utils import secure_filename
from flask_login import login_required, current_user
from ..decorators import admin_required


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

