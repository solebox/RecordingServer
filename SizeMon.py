from threading import Thread

import time

from FFMpeg import FFMpeg


class SizeMon(Thread):

    def __init__(self, ffmpeg, logger):
        super().__init__()
        self.logger = logger
        self.ffmpeg = ffmpeg
        self.logger.info("starting SizeMon for {}".format(self.ffmpeg.destination))
        self.watching = True
        self.current_size = -1
        self.prev_size = -2

    def _file_stuck(self, destination):
        """
        in the event of a stuck file (mid recording) this method is invoked
        :param destination:
        :return:
        """
        self.logger.warning("file {} is stuck mid recording".format(self.ffmpeg.destination))

    def _ffmpeg_failed(self, destination):
        self.logger.warning(" ffmpeg failed recording: {}".format(self.ffmpeg.destination))

    def update_current_size(self, current_size):
        self.logger.debug("updating remote about current size of {} size: {}".format(self.ffmpeg.destination, current_size))

    def run(self):
        self.logger.debug("started watching: {}".format(self.ffmpeg.destination))
        time.sleep(2)
        while self.watching:
            if self.prev_size == self.current_size:
                if self.watching:
                    if self.ffmpeg.is_alive():
                        self._file_stuck(self.ffmpeg.destination)
                    else:  # ffmpeg is already dead man
                        if self.ffmpeg.return_status() != 0:
                            self._ffmpeg_failed(self.ffmpeg.destination)
                        self.watching = False  # aint no body got time for that (stop staring at the dead)
            time.sleep(2)

            self.prev_size = self.current_size
            self.current_size = self.ffmpeg.size()
            self.update_current_size(self.current_size)
        return 0

    def stop(self):
        self.watching = False
