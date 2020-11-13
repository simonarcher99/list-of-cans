# from flask import Flask, render_template, request, redirect, flash, url_for
# from flask_sqlalchemy import SQLAlchemy
# from flask_wtf import FlaskForm
# from wtforms import Form, StringField, PasswordField, SubmitField, BooleanField
# from wtforms.validators import InputRequired, Email, EqualTo, ValidationError
# from flask_login import current_user, login_user, logout_user, login_required, LoginManager, UserMixin
# from werkzeug.security import generate_password_hash, check_password_hash
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate 
from flask_login import LoginManager 

app = Flask(__name__)

from db import db

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cans.db'
app.secret_key = 'simon'
login_manager = LoginManager(app)

from routes import *
from models import *

@app.before_first_request
def create_tables():
    db.create_all()


if __name__ == '__main__':
    db.init_app(app)
    from db import db
    db.init_app(app)
    app.run(host='0.0.0.0', port=5010, debug=True)
