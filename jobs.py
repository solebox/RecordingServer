import os
import re

from flask import Flask
from flask_apscheduler import APScheduler
import time
import random
from FFMpeg import FFMpeg

recording_path = "/home/sole/recordings"


class Config(object):
    JOBS = [
        # {
        #     'id': 'job1',
        #     'func': 'jobs:job1',
        #     'args': (1, 2),
        #     'trigger': 'interval',
        #     'seconds': 10
        # }
    ]

    SCHEDULER_VIEWS_ENABLED = True


def job1(a, b, **kwargs):
    # print(str(a) + ' ' + str(b))
    time.sleep(20)


def record(source, meta_data, timeout=10, **kwargs):
    evil_chars = r"[^a-zA-Z0-9_-]"
    file_name_prefix = meta_data.get("file_name_prefix", "")
    if re.match(evil_chars, file_name_prefix):
        raise TabError("your input is evil and you should feel bad")
    random_name = "{:x}".format(random.getrandbits(128))
    destination = os.path.join(recording_path, file_name_prefix + "_" + random_name)
    ffmpeg = FFMpeg(source, destination, timeout)
    ffmpeg.record()



class RecordingJobScheduler(APScheduler):

    def __init__(self):
        super(RecordingJobScheduler, self).__init__()

    def add_job(self, id, func, **kwargs):
        """
        Adds the given job to the job list and wakes up the scheduler if it's already running.
        :param str id: explicit identifier for the job (for modifying it later)
        :param func: callable (or a textual reference to one) to run at the given time
        """
        ret = super(RecordingJobScheduler, self).add_job(id, func, **kwargs)
        print(id, kwargs)
        return ret

    def delete_job(self, id, jobstore=None):
        """
            Removes a job, preventing it from being run any more.
            :param str id: the identifier of the job
            :param str jobstore: alias of the job store that contains the job
        """
        return super(RecordingJobScheduler, self).delete_job(id, jobstore=None)


if __name__ == "__main__":
    app = Flask(__name__)
    app.config.from_object(Config())
    app.debug = True

    scheduler = RecordingJobScheduler()
    scheduler.init_app(app)
    scheduler.start()
    app.run()