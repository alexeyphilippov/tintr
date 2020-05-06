import os
import sys
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
sys.path.append(os.path.join(basedir, "utils"))
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///" + os.path.join(basedir, "db.sqlite")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

ma = Marshmallow(app)


@app.route('/', methods=['POST', 'GET'])
def hello():
    return "hi"


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='40', debug=True)
