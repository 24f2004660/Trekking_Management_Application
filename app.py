from flask import Flask
from models import db

app = None

#creating configuration between app and database model
def setup_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///trekking.sqlite3'
    db.init_app(app)  #linking between db and flask
    app.app_context().push()  #Giving acces of my current app to other modules
    print("Database connected successfully....setup done...")

#executable flask
setup_app() #calling

from controller import *

if __name__ == '__main__':
    app.run(debug=True)
