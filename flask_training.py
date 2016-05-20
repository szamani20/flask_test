from flask import Flask, request

app = Flask(__name__)


@app.route('/')
def show_all():
    return "Home Page"


@app.route('/new', methods=['GET', 'POST'])
def new():
    json_data = request.get_json()
    data = Data(**json_data)
    return data.name + " " + data.age


class Data:
    def __init__(self, name, age):
        self.name = name
        self.age = age


if __name__ == '__main__':
    app.run(debug=True)
