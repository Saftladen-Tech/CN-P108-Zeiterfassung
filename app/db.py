import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db/database.db')
db = SQLAlchemy(app)

class User(db.Model):
    UID = db.Column(db.String, primary_key=True)
    Name = db.Column(db.String, nullable=False)
    Firstname = db.Column(db.String, nullable=False)
    DOB = db.Column(db.Date, nullable=False)
    CA = db.Column(db.String, db.ForeignKey('class.CA'))

class Login(db.Model):
    NR = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Time = db.Column(db.DateTime, nullable=False)
    UID = db.Column(db.String, db.ForeignKey('user.UID'))

class Logoff(db.Model):
    NR = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Time = db.Column(db.DateTime, nullable=False)
    UID = db.Column(db.String, db.ForeignKey('user.UID'))

class Admin(db.Model):
    Username = db.Column(db.String, primary_key=True)
    Password = db.Column(db.String, nullable=False)
    UID = db.Column(db.String, db.ForeignKey('user.UID'))

class Class(db.Model):
    CA = db.Column(db.String, primary_key=True)
    Subject_area = db.Column(db.String, nullable=False)
    Classroom = db.Column(db.String, nullable=False)

def init_db():
    with app.app_context():
        db.create_all()


if __name__ == '__main__':
    init_db()
