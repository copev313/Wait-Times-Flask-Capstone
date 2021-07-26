from flask_wtf import FlaskForm
from wtforms import (SelectField, StringField, SubmitField, TextAreaField, IntegerField)
from wtforms.validators import DataRequired, Length, URL


status_choices = [('', 'Choose...'), ('CLOSED', 'CLOSED'), ('OPEN', 'OPEN'),
                  ('TESTING', 'TESTING'), ('COMING SOON', 'COMING SOON')]


class UpdateRideForm(FlaskForm):
    '''Form used for updating an existing Ride's information.'''
    
    name = StringField('Name',
                       validators=[DataRequired(), Length(3, 50)],
                       render_kw={"placeholder": "Ride Name"})
    status = SelectField('Status', choices=status_choices)
    image_url = StringField('Image URL', validators=[URL()])
    notes = TextAreaField('Notes')
    submit = SubmitField('Update Ride')



class CreateRideForm(FlaskForm):
    '''Form used for creating a new Ride.'''
    
    name = StringField('Name', validators=[DataRequired(), Length(3, 50)])
    status = SelectField('Status', choices=status_choices, validators=[DataRequired()])
    waittime = IntegerField('Wait Time (Minutes)')
    image_url = StringField('Image URL', validators=[URL()])
    notes = TextAreaField('Notes')
    submit = SubmitField('Create Ride')
