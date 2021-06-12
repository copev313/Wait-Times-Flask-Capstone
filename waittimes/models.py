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
        self.username = username
        self.email = email.lower()
        self.set_password(password)

    def __repr__(self):
        return '<USER {} | {}>'.format(self.username, self.email)

    def create_user_account(self):
        db.session.add(self)
        db.session.commit()

    def delete_user_account(self):
        db.session.delete(self)
        db.session.commit()

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def set_last_login(self):
        self.last_login = dt.utcnow()
        db.session.add(self)
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
    
    def __init__(self, name:str, status:str, waittime:int):
        self.name = name.title()
        self.set_ride_status('COMING SOON')
        self.set_waittime()
        self.set_last_maintenance_date()
        self.set_last_waittime_update()
        

    def __repr__(self):
        return '<RIDE {} | status: {} | waittime: {} >'.format(
            self.name, self.status, self.waittime
        )

    def set_last_maintenance_date(self, date=dt.utcnow()):
        self.last_maintenance_date = date

    def set_last_waittime_update(self, date=dt.utcnow()):
        self.last_waittime_update = date

    def set_ride_status(self, status:str='CLOSED'):
        self.ride_status = status

    def set_waittime(self, minutes:int=1440):
        self.waittime = minutes

    def set_ride_image(self, link_address:str):
        self.ride_image = link_address

    def write_optional_notes(self, notes:str):
        self.optional_notes = notes
