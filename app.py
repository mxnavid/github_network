from flask import Flask, jsonify
from gather import *

# pip install Flask
# export FLASK_APP='app.py'
# flask run

app = Flask(__name__)

@app.route('/')
def index():
    return 'hello, world'

# http://localhost:5000/contributors/react
@app.route('/contributors/<repo>')
def users(repo):
    return jsonify(
        getUsers(f'data/{repo}_contributors.json')
    )

@app.route('/repos.json')
def repos():
    return jsonify(
        getUsers('data/flutter_contributors.json')
    )
