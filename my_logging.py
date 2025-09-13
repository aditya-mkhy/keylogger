from datetime import datetime
import atexit, signal, sys, os
import time
from util import log

class Logger:
    def __init__(self, filename = "log.txt", max_size_mb = 100):
        self.filename = filename
        self.max_size = max_size_mb * 1024 * 1024
        self.file = open(self.filename, "a+", encoding="utf-8")

        # Fail-safe
        atexit.register(self.close)
        signal.signal(signal.SIGTERM, self._handle_exit)
        signal.signal(signal.SIGINT, self._handle_exit)

    

    def _check_rotation(self):
        if self.file and os.path.getsize(self.file.name) >= self.max_size:
            self.close()
            self.file = open(self.filename, "w", encoding="utf-8")  # reset
            self.write("---------------- OpeningFile -----------------")

    def write(self, message, overwrite=False):
        self._check_rotation()

        if overwrite:
            # Move file pointer back and truncate last line
            self.file.seek(self.last_pos)
            self.file.truncate()
      
        message += "\n"

        # Remember position for next overwrite
        self.last_pos = self.file.tell()
        self.file.write(message)
        self.file.flush()

        # Console output (overwrite on screen too)
        if overwrite:
            log(f"\r{message}", end="")
        else:
            log(message, end="")


    def close(self):
        if self.file and not self.file.closed:
            self.file.close()

    def _handle_exit(self, signum, frame):
        self.close()
        sys.exit(0)


if __name__ == "__main__":
    logger = Logger("log.txt")


    logger.write("Task started")
    logger.write("Progress 0%")
    for i in range(0, 101, 10):
        time.sleep(0.05)
        logger.write(f"Progress {i}%", overwrite=True)  # overwrite last line
    logger.write("Task finished")  # new line
    logger.close()
