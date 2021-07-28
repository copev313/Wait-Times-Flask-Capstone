from flask_wtf import FlaskForm
from waittimes.models import User
from wtforms import BooleanField, PasswordField, StringField, SubmitField
from wtforms.validators import (DataRequired, Email, EqualTo, Length, Optional,
                                ValidationError)


class AdminUpdateUserForm(FlaskForm):
    '''Form used by an admin to update a User account.'''

    username = StringField('Username',
                    validators=[Optional(), Length(min=3, max=20)],
                    render_kw={'placeholder': 'Username',
                               'type': 'username' })

    email = StringField('Email',
                validators=[Optional(), Email()],
                render_kw={ 'placeholder': 'Email Address',
                            'type': 'email' })
    
    admin = BooleanField('Is Admin')

    submit = SubmitField('Save Changes')

    def validate_email(self, email):
        '''Validation to make sure the provided email address is unique.'''
        
        user = User.query.filter_by(email=email.data).first()
        # Check if email is already in use:
        if user:
            raise ValidationError("This email address is already in use!")



class AdminCreateUserForm(FlaskForm):
    '''Form used by an admin to create a new User account.'''

    username = StringField('Username',
                    validators=[DataRequired(), Length(min=3, max=20)],
                    render_kw={'placeholder': 'Username',
                               'type': 'username' })                   

    email = StringField('Email',
                validators=[DataRequired(), Email()],
                render_kw={ 'placeholder': 'Email Address',
                            'type': 'email' })

    password = PasswordField('Password',
                    validators=[DataRequired()],
                    render_kw={'placeholder': 'Password',
                                'pattern': '(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,}',
                                'title': "Must contain at least one number, " \
                                    "one uppercase and lowercase letter, and " \
                                    "have at least 8 characters." })

    confirm_password = PasswordField('Confirm Password',
                            validators=[DataRequired(), EqualTo('password')],
                            render_kw={ 'placeholder': 'Confirm Password' })
    
    admin = BooleanField('Is Admin', default=False)

    submit = SubmitField('Create Account')

    def validate_email(self, email):
        '''Validation to make sure the provided email address is unique.'''
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError("This email address is already in use!")


class AdminDeleteUserForm(FlaskForm):
    """Form added to admin edit user screen to remove users."""
    
    email = StringField('Confirm Email',
                        validators=[DataRequired(), Email()],
                         render_kw={'placeholder': 'Confirm Email'})
    submit = SubmitField('Delete Account')