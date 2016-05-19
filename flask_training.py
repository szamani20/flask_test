from flask import Flask, request

app = Flask(__name__)


@app.route('/test', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        return 'Worked POST'
    else:
        return 'Worked GET'


if __name__ == '__main__':
    app.run(debug=True)
