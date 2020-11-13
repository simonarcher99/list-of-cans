from werkzeug.security import generate_password_hash, check_password_hash
from flask import current_app
from flask_login import UserMixin
from app import db

class cans(db.Model):
    __tablename__ = 'cans'
    id = db.Column('can_id', db.Integer, primary_key = True)
    name = db.Column(db.String(50))
    number = db.Column(db.Integer)

    def __init__(self, name, number):
        self.name = name.title()
        self.number = number

class User(db.Model, UserMixin):
    __tablname__ = 'user'
    id = db.Column('user_id', db.Integer, primary_key = True)
    username = db.Column(db.String(20))
    password_hash = db.Column(db.String(100))
    email = db.Column(db.String(40))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User {}>'.format(self.email)

