#!/usr/bin/env python
import json
import sys
import subprocess
from FFMpeg import FFMpeg
from SizeMon import SizeMon
import logging

logging.basicConfig(filename='example.log', level=logging.DEBUG)
logger = logging

if len(sys.argv) != 2:
    print("usage: {} config_file".format(sys.argv[0]))
    sys.exit(1)
conf = {}

with open(sys.argv[1]) as config_file:
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
        date_time = "11.11.placeholder"
        recording_name = "{source_name}_{date_time}".format(source_name=source_name, date_time=date_time)
        recording_name = "/home/sole/recordings/{}.mp4".format(recording_name)
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
            outs, errs = recording_process.communicate(timeout=duration)
            recording_monitors[source_name].stop()
        except subprocess.TimeoutExpired:
            recording_process.kill()
            outs, errs = recording_process.communicate()

except Exception as general_exception:
    logger.error("your configuration file is broken , "
          "please see that you are not breaking"
          " conventions thanks: {}".format(general_exception.with_traceback(general_exception)))
    sys.exit(1)