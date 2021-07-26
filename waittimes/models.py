from datetime import datetime as dt

from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

from waittimes import db, login_manager


class User(db.Model, UserMixin):

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime, default=dt.utcnow)
    last_login = db.Column(db.DateTime)
    username = db.Column(db.String(50), index=True, unique=False)
    email = db.Column(db.String(75), index=True, unique=True)
    password_hash = db.Column(db.String(150))
    is_admin = db.Column(db.Boolean, default=False)

    def __init__(self, username, email, password):
        '''Creates a new User object that can be saved to the database.'''
        self.username = username
        self.email = email.lower()
        self.set_password(password)
        self.last_login = dt.utcnow()

    def __repr__(self):
        '''Returns a string representation of the User object.'''
        return f"<USER {self.username} | {self.email}>"

    def create_user_account(self):
        '''Adds the given user to the database.'''
        db.session.add(self)
        db.session.commit()
    
    def save_changes(self):
        '''Saves the changes made to the User object to the DB.'''
        db.session.commit()

    def delete_user_account(self):
        '''Deletes the given user from the database.'''
        db.session.delete(self)
        db.session.commit()

    def set_password(self, password):
        '''Sets the password to the given User.'''
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        '''Checks if the given password matches the password stored in the 
        database when both are hashed.'''
        return check_password_hash(self.password_hash, password)

    def set_last_login(self):
        '''Sets the last_login property of the given User to the current 
        timestamp and saves changes to the DB.'''
        self.last_login = dt.utcnow()
        db.session.commit()

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))


class Ride(db.Model):

    __tablename__ = 'rides'

    id = db.Column(db.Integer, primary_key=True)
    last_waittime_update = db.Column(db.DateTime, default=dt.utcnow)
    last_maintenance_date = db.Column(db.DateTime)
    name = db.Column(db.String(75), index=True, unique=True, nullable=False)
    status = db.Column(db.String(50), index=False, unique=False)
    waittime = db.Column(db.Integer, index=False, unique=False, nullable=False)
    image = db.Column(db.String(200), index=False, unique=False)
    optional_notes= db.Column(db.String(200), index=False, unique=False)
    
    def __init__(self, name:str, waittime:int=1440):
        self.name = name.title()
        self.set_ride_status('COMING SOON')
        self.set_waittime(waittime)
        self.set_last_maintenance_date()
        self.set_last_waittime_update()
        

    def __repr__(self):
        return '<RIDE {} | status: [{}] | waittime: {}min >'.format(
            self.name, self.status, self.waittime
        )
        
    def create_ride(self):
        db.session.add(self)
        db.session.commit()
    
    def save_changes(self):
        db.session.commit()
        
    def delete_ride(self):
        db.session.delete(self)
        db.session.commit()

    def set_last_maintenance_date(self):
        self.last_maintenance_date = dt.utcnow()

    def set_last_waittime_update(self):
        self.last_waittime_update = dt.utcnow()

    def set_ride_status(self, status:str='CLOSED'):
        self.status = status

    def set_waittime(self, minutes:int=360):
        # Check if the waittime is a valid value:
        if (minutes >= 0) and (minutes <= 1440):
            # Round minutes to the nearest 5 minutes:
            minutes = int(round(minutes / 5) * 5)
            self.waittime = minutes
        # Time is too small, set to 0:
        elif (minutes < 0):
            self.waittime = 0
        # Time is too big, set to 1440:
        else:
            self.waittime = 1440
        

    def set_ride_image(self, link_address:str):
        self.image = link_address

    def write_optional_notes(self, notes:str):
        self.optional_notes = notes
