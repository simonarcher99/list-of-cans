from flask import render_template, request, redirect, flash, url_for
from flask_login import current_user, login_user, logout_user, login_required
from  app import app, db, login_manager
from forms import LoginForm, RegistrationForm
from models import User

@app.route('/')
@app.route('/index')
def index():
    return render_template('home.html', cans = cans.query.order_by(cans.name).all())

@app.route('/add_can', methods =["GET", "POST"])
def add_can():
    if request.method == "POST":
        can = request.form.get("add_can")
        if can:
            new_data = cans(can, 1)
            db.session.add(new_data)
            db.session.commit()
        else:
            return {'message': 'Cannot enter empty string'}
    return redirect('/')
    
@app.route('/item/delete/<id>', methods=['DELETE', 'POST', 'GET'])
def delete(id):
    can = cans.query.get(id)
    db.session.delete(can)
    db.session.commit()
    return redirect('/')

@app.route('/item/add/<id>', methods=['POST'])
def add(id):
    can = cans.query.filter_by(id = id).first()
    can.number += 1
    db.session.commit()
    return redirect('/item/{}'.format(id))

@app.route('/item/eat/<id>', methods=['POST', 'GET'])
def eat(id):
    can = cans.query.get(id)
    if can.number >= 1:
        can.number -= 1
        db.session.commit()
        return redirect('/item/{}'.format(id))
    else:
        return {'Message': 'Silly you there was no {}'.format(can.name)}

@app.route('/item/<id>', methods=['POST', 'GET'])
def item(id):
    return render_template('item.html', item = cans.query.filter_by(id=id).first())

@app.route('/login', methods=['POST', 'GET'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    next_page = request.args.get('next')
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login', net=next_page))
        
        login_user(user, remember=form.remember_me.data)
        flash('You are now logged in')

        if not next_page:
            return redirect(url_for('index'))
    return render_template('login.html', form=form)

@app.route('/register', methods=['POST', 'GET'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Registration succesful')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You are now logged out')
    return redirect(url_for('index'))

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

@app.route('/home', methods=['POST', 'GET'])
@app.route('/item/home', methods=['POST', 'GET'])
def home():
    return redirect('/')