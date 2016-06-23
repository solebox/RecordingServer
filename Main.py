import base64

import flask
from flask import Flask
from flask_login import login_url, LoginManager, UserMixin,login_user
from flask_security import LoginForm
from flask_apscheduler import APScheduler
from flask_hmacauth import hmac_auth, DictAccountBroker, HmacManager

import jobs
from jobs import Config

app = Flask(__name__)


if __name__ == "__main__":


    accountmgr = DictAccountBroker(
        accounts={
            "admin": {"secret": ";hi^897t7utf", "rights": ["create", "edit", "delete", "view"]},
            "editor": {"secret": "afstr5afewr", "rights": ["create", "edit", "view"]},
            "guest": {"secret": "ASDFjoiu%i", "rights": ["view"]}
        })
    hmacmgr = HmacManager(accountmgr, app)

    app.config.from_object(Config())
    app.debug = True

    scheduler = jobs.RecordingJobScheduler()

    scheduler.init_app(app)

    # monkey patching module to use hmac auth
    for function in app.view_functions:
        current = app.view_functions[function]
        app.view_functions[function] = hmac_auth("create")(current)

    scheduler.start()
    app.run()