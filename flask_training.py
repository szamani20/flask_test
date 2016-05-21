from flask import Flask, request, jsonify
import json
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.sqlite3'
app.config['SECRET_KEY'] = "random string"

db = SQLAlchemy(app)


class Person(db.Model):
    id = db.Column('person_id', db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    age = db.Column(db.String(50))

    def dump(self):
        return {'name': self.name,
                'age': self.age}


def __init__(self, name, age):
    self.name = name
    self.age = age


@app.route('/')
def show_all():
    for i in db.session.query(Person).all():
        db.session.delete(i)
        db.session.commit()
    return "Home Page"


@app.route('/new', methods=['GET', 'POST'])
def new():
    json_data = request.get_json()
    person = Person(**json_data)
    db.session.add(person)
    db.session.commit()
    return person.name + " " + person.age


@app.route('/get_all', methods=['GET', 'POST'])
def get_all():
    dicts = []
    for i in db.session.query(Person).all():
        dicts.append(i.dump())
    return json.dumps(dicts)


if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
