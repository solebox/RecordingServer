from flask import Flask
from flask_apscheduler import APScheduler
import jobs
from jobs import Config

if __name__ == "__main__":
    app = Flask(__name__)
    app.config.from_object(Config())
    app.debug = True

    scheduler = jobs.RecordingJobScheduler()
    scheduler.init_app(app)
    scheduler.start()
    app.run()