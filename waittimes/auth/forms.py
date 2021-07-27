from flask_wtf import FlaskForm
from waittimes.models import User
from wtforms import BooleanField, PasswordField, StringField, SubmitField
from wtforms.validators import (DataRequired, Email, EqualTo, Length,
                                ValidationError)


class RegistrationForm(FlaskForm):
    '''Form used for creating a new User account.'''

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

    submit = SubmitField('Create Account')

    def validate_email(self, email):
        '''Validation to make sure the provided email address is unique.'''
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError("This email address is already in use!")



class LoginForm(FlaskForm):
    '''Login form used to provide user authorization.'''

    email = StringField('Email',
                validators=[DataRequired(), Email()],
                render_kw={ 'placeholder': 'Email Address',
                            'type': 'email',
                            'autocomplete': 'email' })

    password = PasswordField('Password',
                validators=[DataRequired()],
                render_kw={ 'placeholder': 'Password',
                            'autocomplete': 'current-password' })

    remember = BooleanField('Remember Me')

    submit = SubmitField('Login')
