import logging
import os


def remove_file(file):
    if os.path.isfile(file):
        os.remove(file)
        logging.debug(f"Removed file {file}")