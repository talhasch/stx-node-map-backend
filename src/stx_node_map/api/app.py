from flask import Flask, jsonify


def __flask_setup():
    global app

    app = Flask(__name__)

    @app.route("/nodes")
    def nodes():
        return jsonify([])


def __run_dev_server():
    global app

    app.config['DEVELOPMENT'] = True
    app.config['DEBUG'] = True

    app.run(host='127.0.0.1', port=8089)


__flask_setup()


def main():
    __run_dev_server()
