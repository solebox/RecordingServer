#!/usr/bin/env python
import json
import sys
import subprocess
from FFMpeg import FFMpeg

from SizeMon import SizeMon
import colorlog
import logging
from datetime import datetime



handler = colorlog.StreamHandler()
handler.setFormatter(colorlog.ColoredFormatter('%(log_color)s%(levelname)s:%(name)s:%(message)s'))

logger = colorlog.getLogger('example')
logger.addHandler(handler)


colorlog.basicConfig(filename='/var/log/recording.log', level=logging.DEBUG)

conf_location = "./conf.json"

conf = {}

with open(conf_location) as config_file:
    conf = json.load(config_file)

try:

    sources = conf["sources"]
    duration = conf["duration"]
    connection_timeout = conf["connection_timeout"]
    recording_procs = {}
    recording_monitors = {}
    for source in sources:

        address = source["address"]
        source_name = source["source_name"]
        date_time = datetime.now().strftime("%H_%M_%S")
        recording_name = "{date_time}_{source_name}".format(source_name=source_name, date_time=date_time)
        recording_name = "/home/sole/recordings/{}".format(recording_name)
        try:
            ffmpeg = FFMpeg(address, recording_name, duration, connection_timeout=connection_timeout)
            logger.info("setting up ffmpeg for {}: {}".format(source_name, ffmpeg.destination))
            recording_proc = ffmpeg.record()
            recording_procs[source_name] = recording_proc
            recording_monitors[source_name] = (SizeMon(ffmpeg, logger))
            recording_monitors[source_name].start()
        except Exception as general_exception:
            logger.error("ffmpeg recording stopped: {} {}".format(recording_name,
                                                           general_exception.with_traceback(general_exception)))

    for source_name, recording_process in recording_procs.items():
        try:
            parsed_duration = datetime.strptime(duration,"%H:%M:%S.%f")
            parsed_duration = parsed_duration.hour * (60**2) + parsed_duration.minute*60 + parsed_duration.second + 100
            outs, errs = recording_process.communicate(timeout=parsed_duration)
            recording_monitors[source_name].stop()
        except subprocess.TimeoutExpired:
            recording_process.kill()
            outs, errs = recording_process.communicate()

except Exception as general_exception:
    logger.error("your configuration file is broken , "
          "please see that you are not breaking"
          " conventions thanks: {}".format(general_exception.with_traceback(general_exception)))
    sys.exit(1)