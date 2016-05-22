from flask import Flask, request
import json
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///login_data.sqlite3'
app.config['SECRET_KEY'] = "random string"

db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column('id', db.Integer, primary_key=True)
    username = db.Column(db.String(100))
    password = db.Column(db.String(50))

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def dump(self):
        return {'username': self.username,
                'password': self.password}


class Channel(db.Model):
    id = db.Column('id', db.Integer, primary_key=True)
    channel_id = db.Column(db.String(50))
    channel_name = db.Column(db.String(100))

    def __init__(self, channel_id, channel_name):
        self.channel_id = channel_id
        self.channel_name = channel_name

    def dump(self):
        return {'channel_id': self.channel_id,
                'channel_name': self.channel_name}


@app.route('/', methods=['GET', 'POST'])
def home_page():
    for user in User.query.all():
        print(user.username, user.password)
    return "Homepage"


@app.route('/add_user', methods=['POST'])
def add_user():
    json_data = request.get_json()
    user = User(**json_data)
    if User.query.filter_by(username=user.username).first() is not None:
        return "Username already taken"
    db.session.add(user)
    db.session.commit()
    return "User " + user.username + " with Password " + user.password + " created"


@app.route('/delete_user', methods=['POST'])
def delete_user():
    json_data = request.get_json()
    user = User(**json_data)
    if User.query.filter_by(username=user.username).first() is not None:
        db.session.delete(User.query.filter_by(username=user.username).first())
        db.session.commit()
        return "User " + user.username + " with password " + user.password + " deleted"
    return "No such user"


@app.route('/get_all_users', methods=['POST'])
def get_all_users():
    all_users = []
    for user in User.query.all():
        all_users.append(user.dump())
    return json.dumps(all_users)


@app.route('/get_user_by_username', methods=['POST'])
def get_user_by_username():
    pass


@app.route('/add_channel', methods=['POST'])
def add_channel():
    json_data = request.get_json()
    channel = Channel(**json_data)
    if Channel.query.filter_by(channel_id=channel.channel_id).first() is not None:
        return "channel already set"
    db.session.add(channel)
    db.session.commit()
    return "Channel " + channel.channel_name + " with ID " + channel.channel_id + " created"


@app.route('/delete_channel', methods=['POST'])
def delete_channel():
    json_data = request.get_json()
    channel = Channel(**json_data)
    if Channel.query.filter_by(channel_id=channel.channel_id).first() is not None:
        db.session.delete(Channel.query.filter_by(channel_id=channel.channel_id).first())
        db.session.commit()
        return "Channel " + channel.channel_id + " with name " + channel.channel_name + " deleted"
    return "No such channel"


@app.route('/get_all_channels', methods=['POST'])
def get_all_channels():
    all_channels = []
    for channel in Channel.query.all():
        all_channels.append(channel.dump())
    return json.dumps(all_channels)


@app.route('/get_channel_by_channel_id', methods=['POST'])
def get_channel_by_channel_id():
    pass


if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
