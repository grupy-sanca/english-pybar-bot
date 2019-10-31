import logging
import sys

class Log:
    def __init__(self):
        logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)

    def log_error(self, error):
        self.logger.error(error)
        sys.exit(1)