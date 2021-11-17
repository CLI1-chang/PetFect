"""
app.main views: render web pages with GET POST operations
Reference: O'Reilly Flask Web Development
"""

from flask import render_template, session, redirect, url_for, flash, jsonify,\
    request, Response
# from wtforms.validators import DataRequired
from . import main
from .. import db
from datetime import datetime
from ..models import Animal, User
from .forms import AnimalForm, NewsForm, animal_list, EditProfileForm,\
    SearchAnimal, EditProfileAdminForm
from werkzeug.utils import secure_filename
from flask_login import login_required, current_user
from ..decorators import admin_required


@main.route('/', methods=['GET', 'POST'])
def index():
    new_animals = Animal.query.order_by(Animal.data_created.desc()).limit(6).all()
    return render_template('index.html', new_animals=new_animals)


@main.route('/about')
def about():
    return render_template("about.html")


@main.route('/animal')
def animal():
    animals = Animal.query.filter(Animal.availability == 'Available').all()
    return render_template("animal.html", animals=animals)


@main.route('/animal/<int:id>')
def single_animal(id):
    curr_animal = Animal.query.get_or_404(id)
    return render_template('_animal.html', animal=curr_animal)


@main.route('/search', methods=['GET', 'POST'])
def search():
    form = SearchAnimal()
    if form.validate_on_submit():
        search_type = form.animal_type.data
        animals = Animal.query.filter(Animal.type == search_type).all()
        return render_template('animal.html', animals=animals)
    return render_template('search.html', form=form)


@main.route('/<int:id>')
def get_img(id):
    img = Animal.query.filter_by(id=id).first()
    if not img:
        return 'No image with that id', 404
    return Response(img.img, mimetype=img.img_mimetype)


@main.route('/contact')
def contact():
    return render_template("contact.html")


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


@main.route('/manage_animal/<int:id>', methods=['GET', 'POST'])
@admin_required
def edit_animal_profile(id):
    admin_user = User.query.get_or_404(id)
    animals = Animal.query.order_by(Animal.data_created).all()
    return render_template('edit_animal_profile.html', admin_user=admin_user, animals = animals)


@main.route('/create_animal/<int:id>', methods=['GET', 'POST'])
@admin_required
def create_animal(id):
    admin_user = User.query.get_or_404(id)
    form = AnimalForm()
    form.breeds.choices = animal_list.get("Cats")
    a_type = form.animal_type.data
    a_breed = form.breeds.data
    with_animal = form.good_with_animal.data
    with_kid = form.good_with_kid.data
    leashed = form.leash_required.data
  
    if a_type and a_breed and form.image.data:
        if with_animal or with_kid or leashed:
            file = request.files[form.image.name]
            #print("Breed is", a_breed)
            animal = Animal(name=form.animal_name.data, 
                            type=form.animal_type.data,
                            breeds=a_breed,
                            good_with_animal=form.good_with_animal.data,
                            good_with_kid=form.good_with_kid.data,
                            leash_required=form.leash_required.data,
                            img=file.read(),
                            img_name=secure_filename(file.filename),
                            img_mimetype=file.mimetype,
                            availability=dict(form.avail.choices).get(form.avail.data),
                            description=form.description.data,
                            owner_id=admin_user.id
                            )
            db.session.add(animal)
            db.session.commit()
            flash('New animal profile successfully created!')
            print(current_user.user_name)
            return redirect(url_for('main.user', user_name=admin_user.user_name))
        else:
            # needs to add in an alert 
            print('Must select a disposition!')
    return render_template('create_animal.html', form=form)

@main.route('/update/<int:id>', methods=['GET', 'POST'])
@admin_required
def update(id):
    form = AnimalForm()
    animal_to_update = Animal.query.get_or_404(id)
    if request.method == "POST":
        animal_to_update.name = request.form['animal_name']
        animal_to_update.type = request.form['animal_type']
        animal_to_update.breeds = request.form['breeds']
        animal_to_update.good_with_animal = form.good_with_animal.data
        animal_to_update.good_with_kid = form.good_with_kid.data
        animal_to_update.leash_required = form.leash_required.data
        animal_to_update.availability = dict(form.avail.choices).get(form.avail.data)
        animal_to_update.description = form.description.data
        try:
            db.session.commit()
            flash('Animal profile updated successfully!')
            return render_template('aedit_animal.html', form = form, animal_to_update = animal_to_update)
        except:
            flash('Error! Problem occurred!')
            return render_template('edit_animal.html', form = form, animal_to_update = animal_to_update)
    return render_template('edit_animal.html', form = form, animal_to_update = animal_to_update)




@main.route('/manage_news/<int:id>', methods=['GET', 'POST'])
@admin_required
def edit_news(id):
    admin_user = User.query.get_or_404(id)
    return render_template('edit_news.html',admin_user=admin_user)

