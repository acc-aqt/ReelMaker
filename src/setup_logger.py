import datetime
import logging
import os
import sys

LOG_LEVEL_INFO = "INFO"
LOG_LEVEL_DEBUG = "DEBUG"
LOG_LEVELS = [LOG_LEVEL_INFO, LOG_LEVEL_DEBUG]
LOG_DIR = "reel-maker-logs"


def setup_logger(loglevel):
    os.makedirs(LOG_DIR, exist_ok=True)
    now_string = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    logfile = f'make_reel_{now_string}.log'
    logging.basicConfig(filename=os.path.join(LOG_DIR, logfile), level=loglevel)
    logging.getLogger().addHandler(logging.StreamHandler(sys.stdout))
