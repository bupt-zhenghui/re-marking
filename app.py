# -*- coding:UTF-8 -*-
from flask import Flask
from flask import render_template
from flask import request

import handler
app = Flask(__name__, static_folder='./static')


@app.route('/')
def hello_world():
    return render_template('index.html')


@app.route('/sample')
def sample():
    user = request.args.get("user")
    return handler.sample_handler(user)


@app.route('/send', methods=["POST"])
def send():
    data = request.form
    # print(data)
    user = data.get('user')
    sample_id = int(data.get('sample_id'))
    form = data.get('form')
    if sample_id != -1:
        handler.update_handler(user, sample_id, form)
    else:
        print(f'user {user} login successfully...')
    return {
        "status": "ok"
    }


@app.route('/validation')
def validation():
    user = request.args.get("user")
    valid = handler.validation_handler(user)
    return {
        "data": {
            "valid": valid
        },
        "status": 'ok'
    }


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=6067)
