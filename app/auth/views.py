"""
main.auth views: render auth related web pages with GET POST operations
Reference: O'Reilly Flask Web Development
"""

from flask import render_template, redirect, request, url_for, flash
from flask_login import login_user, logout_user, login_required
from . import auth
from app import db
from app.models import User
from app.auth.forms import LoginForm, RegistrationForm


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data.lower()).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            next = request.args.get('next')
            if next is None or not next.startswith('/'):
                next = url_for('main.petfect')
            return redirect(next)
        flash('Invalid email or password.')
    return render_template('auth/login.html', form=form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('main.petfect'))


@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data.lower(),
                    user_name=form.username.data,
                    password=form.password.data,
                    role_id=form.role.data)
        db.session.add(user)
        db.session.commit()
        flash('You can login now.')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', form=form)
