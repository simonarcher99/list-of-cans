from flask import current_app
from flask_login import UserMixin
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash, check_password_hash
from . import db

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), index=True, unique=True, nullable=False)
    password_hash = db.Column(db.String(100))
    update_date = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    create_date = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    cans = db.relationship('Cans', lazy='dynamic')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return '<User {}>'.format(self.email)

class Cans(db.Model):
    __tablename__ = 'cans'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    number = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship('User')

    def __init__(self, name, number, user_id):
        self.name = name.title()
        self.number = number
        self.user_id = user_id