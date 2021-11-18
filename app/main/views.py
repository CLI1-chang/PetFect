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
from ..models import Animal, User, Association
from .forms import AnimalForm, ContactForm, NewsForm, animal_list, EditProfileForm,\
    SearchAnimal, SearchType, dispos_list, search_breed, avail_dict
from werkzeug.utils import secure_filename
from flask_login import login_required, current_user
from ..decorators import admin_required
import pandas as pd


@main.route('/', methods=['GET', 'POST'])
def index():
    new_animals = Animal.query.order_by(Animal.data_created.desc()).limit(6).all()
    return render_template('index.html', new_animals=new_animals)


@main.route('/about')
def about():
    return render_template("about.html")


@main.route('/animal', methods=['GET', 'POST'])
def animal():
    form1 = SearchType()
    form2 = SearchAnimal()
    form2.animal_breed.choices = search_breed.get('default')
    if form1.validate_on_submit():
        type = form1.animal_type.data
        form2.animal_breed.choices = search_breed.get(type)
        if type != 'Choose':
            filter_1 = Animal.type == type
            animals = Animal.query.filter(filter_1).all()
        else:
            animals = Animal.query.filter(Animal.availability == 'Available').all()
        return render_template('animal.html', form1=form1, form2=form2, animals=animals)

    if form2.is_submitted():
        breed = form2.animal_breed.data
        filter_2 = Animal.breeds == breed
        dispos = dispos_list[form2.animal_dispos.data]
        if dispos == 1:
            filter_3 = Animal.good_with_animal.is_(True)
        elif dispos == 2:
            filter_3 = Animal.good_with_kid.is_(True)
        elif dispos == 3:
            filter_3 = Animal.leash_required.is_(True)
        if breed != 'Choose' and dispos != 0:
            animals = Animal.query.filter(filter_2).filter(filter_3).all()
        elif breed != 'Choose' and dispos == 0:
            animals = Animal.query.filter(filter_2).all()
        elif breed == 'Choose' and dispos != 0:
            animals = Animal.query.filter(filter_3).all()
        else:
            animals = Animal.query.filter(Animal.availability == 'Available').all()
        return render_template('animal.html', form1=form1, form2=form2, animals=animals)

    animals = Animal.query.filter(Animal.availability == 'Available').all()
    return render_template("animal.html", form1=form1, form2=form2, animals=animals)


@main.route('/animal/<int:id>')
def single_animal(id):
    curr_animal = Animal.query.get_or_404(id)
    return render_template('_animal.html', animal=curr_animal)


@main.route('/<int:user_id>/<int:animal_id>', methods=['GET', 'POST'])
def like(user_id, animal_id):
    curr_animal = Animal.query.get_or_404(animal_id)
    res = [user_id, animal_id]
    associations = Association.query.all()
    for instance in associations:
        if res == [instance.user_id, instance.animal_id] and instance.like is True:
            flash('Already liked!')
            return render_template('_animal.html', animal=curr_animal)
        elif res == [instance.user_id, instance.animal_id] and instance.like is not True:
            instance.like = True
            db.session.commit()
            return render_template('_animal.html', animal=curr_animal)
    asso = Association()
    asso.user_id = user_id
    asso.animal_id = animal_id
    asso.like = True
    db.session.add(asso)
    db.session.commit()
    return render_template('_animal.html', animal=curr_animal)


@main.route('/user_like/<int:user_id>/<int:animal_id>', methods=['GET', 'POST'])
def user_like(user_id, animal_id):
    curr_user = User.query.get_or_404(user_id)
    like_item = Association.query.filter_by(user_id=user_id).filter_by(
        animal_id=animal_id).first_or_404()
    like_item.like = True
    db.session.commit()
    animal_list = db.session.query(Animal, Association).\
        join(Association, Association.animal_id == Animal.id).filter_by(
        user_id=user_id).all()
    return render_template('user.html', user=curr_user, animals=animal_list)


@main.route('/unlike/<int:user_id>/<int:animal_id>', methods=['GET', 'POST'])
def unlike(user_id, animal_id):
    curr_user = User.query.get_or_404(user_id)
    unlike_item = Association.query.filter_by(user_id=user_id).filter_by(
        animal_id=animal_id).first_or_404()
    unlike_item.like = False
    db.session.commit()
    animal_list = db.session.query(Animal, Association). \
        join(Association, Association.animal_id == Animal.id).filter_by(
        user_id=user_id).all()
    return render_template('user.html', user=curr_user, animals=animal_list)


@main.route('/date/<int:user_id>/<int:animal_id>', methods=['GET', 'POST'])
def date(user_id, animal_id):
    curr_user = User.query.get_or_404(user_id)
    curr_animal = Animal.query.get_or_404(animal_id)
    return render_template('date.html', user=curr_user, animal=curr_animal)


@main.route('/dated/<int:user_id>/<int:animal_id>', methods=['GET', 'POST'])
def dated(user_id, animal_id):
    curr_animal = Animal.query.get_or_404(animal_id)
    if curr_animal.availability != 'Available':
        flash('Animal is not available! Please try later!')
    res = [user_id, animal_id]
    associations = Association.query.all()
    for instance in associations:
        if res == [instance.user_id,
                   instance.animal_id] and instance.date is True:
            flash('Already dated!')
            return render_template('_animal.html', animal=curr_animal)
        elif res == [instance.user_id,
                     instance.animal_id] and instance.date is not True:
            instance.date = True
            db.session.commit()
            flash('Request sent! Hope to meet the perfect one!')
            return render_template('_animal.html', animal=curr_animal)
    asso = Association()
    asso.user_id = user_id
    asso.animal_id = animal_id
    asso.date = True
    db.session.add(asso)
    db.session.commit()
    flash('Request sent! Hope to meet the perfect one!')
    return render_template('_animal.html', animal=curr_animal)


@main.route('/<int:id>')
def get_img(id):
    img = Animal.query.filter_by(id=id).first()
    if not img:
        return 'No image with that id', 404
    return Response(img.img, mimetype=img.img_mimetype)


@main.route('/contact', methods=["GET", "POST"])
def contact():
    form = ContactForm()
    if request.method == 'POST':
        name = request.form["name"]
        email = request.form["email"]
        subject = request.form["subject"]
        message = request.form["message"]
        time_stamp = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        res = pd.DataFrame({'name': name, 'email': email, 'subject': subject, 'message': message, 'timestamp': time_stamp}, index=[0])
        res.to_csv('app/static/messages/contact_message_{}_{}_{}.csv'.format(name, email, time_stamp))
        return render_template('contact.html', form=form)
    else:
        return render_template('contact.html', form=form)


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
    curr_user_id = curr_user.id
    animal_list = db.session.query(Animal, Association).join(Association, Association.animal_id == Animal.id).filter_by(user_id=curr_user_id).all()
    return render_template('user.html', user=curr_user, animals=animal_list)


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
def manage_animal_profile(id):
    admin_user = User.query.get_or_404(id)
    animals = Animal.query.order_by(Animal.data_created).all()
    return render_template('manage_animal_profile.html', admin_user=admin_user, animals = animals)


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
    flash('Disposition can not be left blank!')
    return render_template('create_animal.html', form=form)

@main.route('/update/<int:id>', methods=['GET', 'POST'])
@admin_required
def update(id):
    animal_to_update = Animal.query.get_or_404(id)
    admin_user = User.query.get_or_404(animal_to_update.owner_id)
    form = AnimalForm()
    animals = Animal.query.order_by(Animal.data_created).all()
    img = Animal.query.filter_by(id=id).first()

    if request.method == "POST":
        file = request.files[form.image.name]
        animal_to_update.name = form.animal_name.data
        animal_to_update.type = form.animal_type.data
        animal_to_update.breeds = form.breeds.data
        animal_to_update.good_with_animal = form.good_with_animal.data
        animal_to_update.good_with_kid = form.good_with_kid.data
        animal_to_update.leash_required = form.leash_required.data
        if file.filename == '':
            flash('No change in picture!')
        else:
            animal_to_update.img=file.read()
            animal_to_update.img_name=secure_filename(file.filename)
            animal_to_update.img_mimetype=file.mimetype
        animal_to_update.availability = dict(form.avail.choices).get(form.avail.data)
        animal_to_update.description = form.description.data
        db.session.commit()
        flash('Animal profile updated successfully!')
        return redirect(url_for('.manage_animal_profile', id= animal_to_update.owner_id, admin_user=admin_user, animals = animals))

    elif request.method == "GET":
        form.animal_type.data = animal_to_update.type
        form.breeds.choices = animal_list.get(animal_to_update.type)
        form.breeds.data = animal_to_update.breeds
        form.good_with_animal.data = animal_to_update.good_with_animal
        form.good_with_kid.data = animal_to_update.good_with_kid
        form.leash_required.data = animal_to_update.leash_required
        form.avail.data = avail_dict.get(animal_to_update.availability)
        form.description.data = animal_to_update.description
    flash('Update unsuccessful, try again!')
    return render_template('edit_animal.html', form = form, animal_to_update = animal_to_update)


@main.route('/delete_animal/<int:id>', methods=['POST'])
@admin_required
def delete_animal(id):
    animal_to_delete = Animal.query.get_or_404(id)
    admin_user = User.query.get_or_404(animal_to_delete.owner_id)
    animals = Animal.query.order_by(Animal.data_created).all()
    db.session.delete(animal_to_delete)
    db.session.commit()
    flash("Successfully deleted the animal profile!")
    return redirect(url_for('.manage_animal_profile', id=animal_to_delete.owner_id, admin_user=admin_user, animals = animals))


@main.route('/manage_news/<int:id>', methods=['GET', 'POST'])
@admin_required
def edit_news(id):
    admin_user = User.query.get_or_404(id)
    return render_template('edit_news.html',admin_user=admin_user)

