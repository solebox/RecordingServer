import requests
from flask import json
import random


class Client(object):

    """
        this is the rest API client abstraction, it is well documented dont be shy to use it

    """
    def __init__(self, recording_server):
        self.recording_server = recording_server

    def run_job(self, job_name, func, *args):
        job_id = "%032x" % random.getrandbits(128)
        job_name = job_name
        func = func
        args = args
        payload = {
            job_id : job_id,
            job_name: job_name,
            func: func,
            args: args
        }
        serializaed_payload = json.dumps(payload)
        requests.post(self.recording_server, serializaed_payload)

    def record_once(self, source, start_time, end_time):
        """
            this job records a video from a given stream , delimited by user specified times
        :param source: the source url
        :param start_time: the time in which the recording will start
        :param end_time: the time is which the recording will stop
        :return:
        """

        command = {"id": job_id}
        requests.get()
        pass

    def repeating_recording(self, source, interval, duration):
        """
         a repeating recording job, every x seconds a recording of y duration will start
        :param source: the url from which we want to record
        :param interval: the time between each recording start
        :param duration: the duration of each recording (take into account that if the duration is larger than the
        interval there will be multiple recordings in parallel)
        :return:
        """
        pass

    def rolling_recording(self, source, file_size):
        """
        this is a function incharge of a continuously rolling recording of a given source
        :param source: the url to record from
        :param file_size: the maximum recording size (take video quality into consideration)
        :return:
        """
        pass
