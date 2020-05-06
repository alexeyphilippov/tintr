import os
import json
from flask import Flask, request, jsonify
from services.getlastones import get_last_ones
from utils.logger import log

app = Flask(__name__)
DATA_DIR = "./data"


@app.route('/data/slice', methods=['GET'])
def hello():
    resp = get_last_ones()
    return json.dumps(resp) if resp else 'Там хуйня какая-то у них в тинькове на сервере'


@app.route('/data/history/<year>/<month>', methods=['GET'])
def get_data(year, month):
    file_path = os.path.join(DATA_DIR, year, month + ".csv")
    try:
        with open(file_path, 'r') as file:
            line = file.read()
            return line
    except Exception as e:
        log("Exception in get_data " + str(e))
        return "Смотри, если месяц пишешь, не пиши нуль в начале"


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='40', debug=True)
