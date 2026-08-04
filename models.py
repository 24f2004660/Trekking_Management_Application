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
    # status = db.Column(db.Integer, nullable=False, default = 0)

class staff_profile(db.Model):
    __tablename__ = 'staff_profile'
    id = db.Column(db.Integer, primary_key=True)
    staff_id = db.Column(db.Integer, db.ForeignKey('user_credentials.id'), nullable=False) #linking user credentials to staff
    name = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(200), nullable=False)
    phone_number = db.Column(db.String(20), nullable=False)
    status = db.Column(db.Integer, nullable=False, default = 0) #0-registered(pending), 1-approved, 2-rejected, 