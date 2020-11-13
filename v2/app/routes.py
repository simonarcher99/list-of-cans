from flask import render_template, redirect, url_for, flash, request
from flask_login import current_user, login_user, logout_user, login_required
from . import app, db, login_manager
from .forms import LoginForm, RegistrationForm
from .models import User, Cans

@app.route('/')
@app.route('/index')
def index():
    if current_user.is_authenticated:
        user_id = current_user.id
        cans = Cans.queryorder_by(cans.name).filter_by(user_id=user_id).all()
        return render_template('user-home.html', cans=cans)
    else:
        return render_template('welcome.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    next_page = request.args.get('next')
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login', next=next_page))

        login_user(user, remember=form.remember_me.data)
        flash('You are now logged in')

        if not next_page:
            cans = Cans.query.filter_by(user_id=user.id).all()
            return render_template('user-home.html', cans = cans)
        return redirect(url_for(next_page))

    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You are now logged out')
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Registration successful')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@login_manager.unauthorized_handler
def unauthorized():
    flash('You must be logged in to view this page')
    return redirect(url_for('login', next=request.endpoint))

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

@app.route('/add_can', methods =["GET", "POST"])
@login_required
def add_can():
    if request.method == "POST":
        can = request.form.get("add_can")
        user_id = current_user.id
        if can:
            new_data = Cans(can, 1, user_id)
            db.session.add(new_data)
            db.session.commit()
        else:
            return {'message': 'Cannot enter empty string'}
        cans = Cans.query.filter_by(user_id=user_id).all()
    return render_template('user-home.html', cans=cans)

@app.route('/item/<id>', methods=['POST', 'GET'])
@login_required
def item(id):
    item = Cans.query.filter_by(id=id).first()
    return render_template('item.html', item = item)

@app.route('/item/add/<id>', methods=['POST'])
@login_required
def add(id):
    can = Cans.query.filter_by(id = id).first()
    can.number += 1
    db.session.commit()
    return redirect('/item/{}'.format(id))

@app.route('/item/eat/<id>', methods=['POST', 'GET'])
@login_required
def eat(id):
    can = Cans.query.get(id)
    if can.number >= 1:
        can.number -= 1
        db.session.commit()
        return redirect('/item/{}'.format(id))
    else:
        return {'Message': 'Silly you there was no {}'.format(can.name)}

@app.route('/item/delete/<id>', methods=['DELETE', 'POST', 'GET'])
@login_required
def delete(id):
    can = Cans.query.get(id)
    db.session.delete(can)
    db.session.commit()
    return redirect('/')