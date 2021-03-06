"""
app models: project database tables implementation
Reference: O'Reilly Flask Web Development
"""

from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import db, login_manager
from datetime import datetime


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship('User', backref='role', lazy='dynamic')

    def __repr__(self):
        return '<Role %r>' % self.name

    @staticmethod
    def insert_roles():
        roles = {'Admin', 'User'}
        for r in roles:
            role = Role.query.filter_by(name=r).first()
            if role is None:
                role = Role(name=r)
            db.session.add(role)
        db.session.commit()


class Association(db.Model):
    __tablename__ = 'association'
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id'), primary_key=True)
    animal_id = db.Column(db.Integer(), db.ForeignKey('animals.id'), primary_key=True)
    like = db.Column(db.Boolean)
    date = db.Column(db.Boolean)
    animal = db.relationship('Animal', back_populates='user')
    user = db.relationship('User', back_populates='user_animal')


class Animal(db.Model):
    __tablename__ = 'animals'
    # primary key of animal
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    type = db.Column(db.String(64),  nullable=False)
    breeds = db.Column(db.String(64), nullable=False)
    # check box for disposition
    good_with_animal = db.Column(db.Boolean, nullable=False)
    good_with_kid = db.Column(db.Boolean, nullable=False)
    leash_required = db.Column(db.Boolean, nullable=False)
    # availability
    availability = db.Column(db.String(64), nullable=False)
    # image to be saved 
    img = db.Column(db.Text, nullable=False)
    img_name = db.Column(db.Text, nullable=False)
    img_mimetype = db.Column(db.Text, nullable = False)
    # description
    description = db.Column(db.String(200), nullable=False)
    data_created = db.Column(db.DateTime, default=datetime.utcnow)
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship('Association', back_populates='animal', cascade="all,delete")

    def __repr__(self):
        return '<Animal %r>' % self.id

class News(db.Model):
    __tablename__ = 'news'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64),unique= True, nullable=False)
    description = db.Column(db.String(200), nullable=False)
    date = db.Column(db.DateTime(), default=datetime.utcnow())
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'))


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    user_name = db.Column(db.String(64), unique=True, index=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    password_hash = db.Column(db.String(128))
    name = db.Column(db.String(64))
    location = db.Column(db.String(64))
    about_me = db.Column(db.Text())
    member_since = db.Column(db.DateTime(), default=datetime.utcnow())

    animals = db.relationship('Animal', backref='owner', lazy='dynamic')
    news = db.relationship('News', backref='owner', lazy='dynamic')
    user_animal = db.relationship('Association', back_populates='user')
    # def __init__(self, **kwargs):
    #     super(User, self).__init__(**kwargs)
    #     if self.role is None:
    #         self.role = Role.query.filter_by(id=2).first()

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def is_administrator(self):
        return self.role_id is not None and (self.role_id == 1)

    def is_user(self):
        return self.role_id is not None and (self.role_id == 2)

    def __repr__(self):
        return '<User %r>' % self.user_name


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
