from flask_wtf import FlaskForm
from wtforms import widgets, StringField, SubmitField, SelectField,SelectMultipleField, FileField,TextAreaField
from wtforms.validators import DataRequired


class NameForm(FlaskForm):
    name = StringField('Please tell us your name', validators=[DataRequired()])
    submit = SubmitField('Submit')

class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=True)
    option_widget = widgets.CheckboxInput()


dispositions = [('1','Good with other animals'), ('2','Good with children'), ('3','Animal must be leashed at all times')]
avail_status = [('1','Not Available'), ('2','Available'), ('3','Pending'),('4','Adopted') ]
animal_list = [('1', 'Cat'), ('2', 'Dogs'), ('3', 'Others')]
breed_list = [('1', 'Cat'), ('2', 'Dogs'), ('3', 'Others')]
class AnimalForm(FlaskForm):
    animal_name = StringField('What is her/his name?',validators=[DataRequired()] )
    animal_type = SelectField('Animal Type', choices =animal_list)
    breeds = SelectField('Breeds', choices =breed_list) 
    disposition = MultiCheckboxField('Disposition', choices=dispositions,validators=[])
    avail= SelectField('Availability', choices=avail_status)
    image = FileField('Upload an image', validators=[])
    description= TextAreaField('Description',validators=[DataRequired()])
    submit = SubmitField('Submit')
