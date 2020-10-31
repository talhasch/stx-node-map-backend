import json
import os

from flask import Flask, jsonify
from flask_cors import CORS

from stx_node_map.util import file_read, assert_env_vars

this_dir = os.path.abspath(os.path.dirname(__file__))
file_path = os.path.join(this_dir, "..", "..", "..", "data.json")


def __flask_setup():
    global app

    app = Flask(__name__)
    CORS(app)

    @app.route("/")
    def index():
        try:
            data = json.loads(file_read(file_path))
        except FileNotFoundError:
            data = []

        resp = {
            "network": assert_env_vars("NETWORK"),
            "nodes": data
        }

        return jsonify(resp)


def __run_dev_server():
    global app

    app.config['DEVELOPMENT'] = True
    app.config['DEBUG'] = True

    app.run(host='127.0.0.1', port=8089)


__flask_setup()


def main():
    __run_dev_server()
