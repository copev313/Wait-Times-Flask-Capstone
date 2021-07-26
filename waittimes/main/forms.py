from flask_wtf import FlaskForm
from flask_login import current_user
from waittimes.models import User
from wtforms import PasswordField, StringField, SubmitField
from wtforms.validators import (DataRequired, Email, EqualTo, Length,
                                ValidationError)


class UpdateAccountForm(FlaskForm):
    '''Form used for updating a User account.'''

    username = StringField('Username',
                    validators=[DataRequired(), Length(min=3, max=16)],
                    render_kw={'placeholder': 'Username',
                               'type': 'username' })

    email = StringField('Email',
                validators=[DataRequired(), Email()],
                render_kw={ 'placeholder': 'Email Address',
                            'type': 'email' })

    password = PasswordField('Password',
                    render_kw={ 'placeholder': 'Password',
                                'pattern': '(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,}',
                                'title': "Must contain at least one number, " \
                                    "one uppercase and lowercase letter, and " \
                                    "have at least 8 characters." })

    confirm_password = PasswordField('Confirm Password',
                            validators=[EqualTo('password')],
                            render_kw={ 'placeholder': 'Confirm Password' })

    submit = SubmitField('Update')
    
    def validate_email(self, email):
        '''Validation to make sure the provided email address is unique.'''
        # User has changed email:
        if (email.data != current_user.email):
            user = User.query.filter_by(email=email.data).first()
            # Check if email is already in use:
            if user:
                raise ValidationError("This email address is already in use!")
