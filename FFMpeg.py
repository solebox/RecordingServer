#!/usr/bin/env python
import json
import os
import subprocess
from datetime import datetime
import sys


class FFMpeg(object):

    def __init__(self, source, destination, duration="00:00:20.000", connection_timeout=1000000, *args, **kwargs):
        super(FFMpeg, self).__init__(*args, **kwargs)
        self.ffmpeg = "/usr/bin/ffmpeg"
        self.source = source
        self.destination = destination + ".mp4"
        self.duration = datetime.strptime(duration, "%H:%M:%S.%f")
        codec = "libx264"
        preset = "medium"
        resolution = "1920x1200"
        vide_buffer = "400k"
        format = "avi"
        audio_codec = ["aac", "-strict", "-2", "-ab", "48k", "-ac", "2", "-ar", "44100"]
        self.ffmpeg_command = [self.ffmpeg, "-y", "-timeout", str(connection_timeout),  "-i", self.source, "-t", self.duration.strftime("%H:%M:%S.%f"), "-vcodec", codec, "-preset:v", preset, "-s",
                               resolution, "-b:v", vide_buffer, "-acodec"] + audio_codec +\
                              ['-f', format, self.destination]

        self.complete_object_for_ffmpeg_run = None
        self.ffmpeg_process = None


    @property
    def pid(self):
        return self.complete_object_for_ffmpeg_run.pid

    def record(self, **kwargs):
        """
        start recording stream , if timeout == 0 record forever
        :param source: url/path
        :param destination: path
        :param timout: the amount of time to record
        :return: pid of the ffmpeg recording proc in session
        """
        source = kwargs.get("source", self.source)
        destination = kwargs.get("destination", self.destination)
        timeout_delta = kwargs.get("timeout", 2)  # time after end of recording in which presumed stuck/done
        timeout = timeout_delta + self.duration.second + self.duration.minute * 60 + self.duration.hour * (60**2)
        print("executing {}".format(self.ffmpeg_command))
        self.ffmpeg_process = subprocess.Popen(self.ffmpeg_command, shell=False)
        return self.ffmpeg_process

    def size(self):
        """
        get current destination file_size
        :return: the size of the file being currently generated by ffmpeg
        """
        try:
            size = os.stat(self.destination).st_size
        except Exception as general_exception:
            size = 0
        return size

    def stop_recording(self):
        """
        kills the recording process
        :return:
        """
        self.complete_object_for_ffmpeg_run.kill()

    def is_alive(self):
        return self.ffmpeg_process.poll() is None

    def return_status(self):
        return self.ffmpeg_process.poll()


if __name__ == "__main__":
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
        recording_procs = []
        for source in sources:

            address = source["address"]
            source_name = source["source_name"]
            date_time = "11.11.placeholder"
            recording_name = "{source_name}_{date_time}".format(source_name=source_name, date_time=date_time)
            recording_name = "/home/sole/recordings/{}.mp4".format(recording_name)
            try:
                ffmpeg = FFMpeg(address, recording_name, duration, connection_timeout=connection_timeout)
                recording_proc = ffmpeg.record()
                recording_procs.append(recording_proc)
            except Exception as general_exception:
                print("ffmpeg recording stopped: {} {}".format(recording_name,
                                                             general_exception))

        for recording_process in recording_procs:
            try:
                outs, errs = recording_process.communicate(timeout=duration)
            except subprocess.TimeoutExpired:
                recording_process.kill()
                outs, errs = recording_process.communicate()

    except Exception as general_exception:
        print("your configuration file is broken , "
              "please see that you are not breaking"
              " conventions thanks: {}".format(general_exception.with_traceback(general_exception)))
        sys.exit(1)
