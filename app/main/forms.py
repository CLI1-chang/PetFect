"""
app.main forms: forms except for auth
Reference: O'Reilly Flask Web Development
"""

from flask_wtf import FlaskForm
from wtforms import widgets, StringField, SubmitField, SelectField, \
    SelectMultipleField, FileField, TextAreaField, BooleanField
from wtforms.validators import DataRequired


class NameForm(FlaskForm):
    name = StringField('Please tell us your name', validators=[DataRequired()])
    submit = SubmitField('Submit')


class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=True)
    option_widget = widgets.CheckboxInput()


dispositions = [('1', 'Good with other animals'),
                ('2', 'Good with children'),
                ('3', 'Animal must be leashed at all times')]
avail_status = [('1', 'Not Available'), ('2', 'Available'),
                ('3', 'Pending'),('4', 'Adopted')]
animal_list = {'Cats':['Ragdoll', 'British Shorthair'],
                'Dogs':['Golden Retriever', 'Pug'],
                'Others':['Hamster1', 'Reptile']}

class AnimalForm(FlaskForm):
    animal_name = StringField('What is her/his name?', validators=[DataRequired()])
    types = list(animal_list.keys())               
    animal_type = SelectField('Animal Type', choices =types)
    breeds = SelectField('Breeds', choices=[])
    good_with_animal = BooleanField('Good with other animals')
    good_with_kid = BooleanField('Good with children')
    leash_required = BooleanField('Animal must be leashed at all times')
    avail= SelectField('Availability', choices=avail_status)
    image = FileField('Upload an image', validators=[])
    description= TextAreaField('Description', validators=[DataRequired()])
    submit = SubmitField('Submit')


class NewsForm(FlaskForm):
    news_title = StringField('What is this news about?', validators=[DataRequired()])
    description= TextAreaField('Description',validators=[DataRequired()])
    image = FileField('Upload an image', validators=[])
    submit = SubmitField('Submit')


class EditProfileForm(FlaskForm):
    name = StringField('Real Name', validators=[DataRequired()])
    location = StringField('Location', validators=[DataRequired()])
    about_me = TextAreaField('About me')
    submit = SubmitField('Submit')


class EditProfileAdminForm(FlaskForm):
    name = StringField('Real name', validators=[DataRequired()])
    location = StringField('Location', validators=[DataRequired()])
    about_me = TextAreaField('About me')
    submit = SubmitField('Submit')
