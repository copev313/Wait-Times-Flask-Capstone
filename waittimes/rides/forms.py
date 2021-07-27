from flask_wtf import FlaskForm
from wtforms import (IntegerField, SelectField, StringField, SubmitField,
                     TextAreaField)
from wtforms.validators import URL, DataRequired, Length, ValidationError

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
    
    def validate_status(self, status):
        '''Validates that the status is a valid choice.'''
        if status.data == '':
            raise ValidationError('Invalid status selected.')



class CreateRideForm(FlaskForm):
    '''Form used for creating a new Ride.'''
    
    name = StringField('Name', validators=[DataRequired(), Length(3, 50)])
    status = SelectField('Status', choices=status_choices, validators=[DataRequired()])
    waittime = IntegerField('Wait Time (Minutes)')
    image_url = StringField('Image URL', validators=[URL()])
    notes = TextAreaField('Notes')
    submit = SubmitField('Create Ride')
