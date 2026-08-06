from datetime import date

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User_Credentials(db.Model):
    __tablename__ = 'user_credentials' #user defined table name
    id =db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    role = db.Column(db.String(20), nullable=False) #allowed only 3 values admin 0, staff 1, user 2

    #Relation column linking parent to child, eg: linking to user_profile
    user = db.relationship('user_profile', cascade="all, delete", backref='user_credentials')

    #Relation column linking parent to child, eg: linking to staff_profile
    staff = db.relationship('staff_profile', cascade="all, delete", backref='user_credentials')
 

class user_profile(db.Model):
    __tablename__ = 'user_profile'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user_credentials.id'), nullable=False) #linking user credentials to trek
    name = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(200), nullable=False)
    phone_number = db.Column(db.String(20), nullable=False) 
    status = db.Column(db.Integer, nullable=False, default = 0)

    bookings = db.relationship('Booking', backref='trekker')

class staff_profile(db.Model):
    __tablename__ = 'staff_profile'
    id = db.Column(db.Integer, primary_key=True)
    staff_id = db.Column(db.Integer, db.ForeignKey('user_credentials.id'),unique = True, nullable=False) #linking user credentials to staff
    name = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(200), nullable=False)
    phone_number = db.Column(db.String(20), nullable=False)
    experience = db.Column(db.String(100), nullable=False)
    status = db.Column(db.Integer, nullable=False, default = 0) #0-registered(pending), 1-approved, 2-rejected, 

    treks = db.relationship('Trek', backref='assigned_staff')


class Trek(db.Model):
    __tablename__ = 'trek'

    trek_id = db.Column(db.Integer, primary_key=True)
    t_name = db.Column(db.String(120), nullable=False)
    location = db.Column(db.String(120), nullable=False)
    diff = db.Column(db.String(1))  # E/M/H
    duration = db.Column(db.Integer)
    avl_slots = db.Column(db.Integer, nullable=False)
    assign_s_id = db.Column(db.Integer, db.ForeignKey('staff_profile.staff_id'), nullable=False)
    status = db.Column(db.String(20), default='Pending')  # Pending/Approved/Open/Close/Completed
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    description = db.Column(db.String(500))

    bookings = db.relationship('Booking', backref='trek')


class Booking(db.Model):
    __tablename__ = 'booking'

    booking_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user_profile.user_id'), nullable=False)
    trek_id = db.Column(db.Integer, db.ForeignKey('trek.trek_id'), nullable=False)
    booking_date = db.Column(db.Date, default=date.today)
    status = db.Column(db.String(20), default='Booked')  # Booked/cancelled/completed
