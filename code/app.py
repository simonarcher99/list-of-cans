from flask import Flask, render_template, request, redirect, flash
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config ['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cans.db'
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.secret_key = 'simon'
db = SQLAlchemy(app)

class cans(db.Model):
    __tablename__ = 'cans'
    id = db.Column('can_id', db.Integer, primary_key = True)
    name = db.Column(db.String(50))
    number = db.Column(db.Integer)

    def __init__(self, name, number):
        self.name = name
        self.number = number


@app.route('/')
def get():
    return render_template('home.html', cans = cans.query.all())

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
    
@app.route('/delete/<id>', methods=['DELETE', 'POST', 'GET'])
def delete(id):
    can = cans.query.get(id)
    db.session.delete(can)
    db.session.commit()
    return redirect('/')

@app.route('/add/<id>', methods=['POST'])
def add(id):
    can = cans.query.filter_by(id = id).first()
    can.number += 1
    db.session.commit()
    return redirect('/')

@app.route('/eat/<id>', methods=['POST', 'GET'])
def eat(id):
    can = cans.query.get(id)
    can.number -= 1
    db.session.commit()
    return redirect('/')


if __name__ == '__main__':
    db.create_all()
    app.run(host='0.0.0.0', port=5010, debug=True)

