import argparse
import datetime
import logging
import os
import sys

from BeatEvaluator import BeatEvaluator
from ImageScaler import ImageScaler
from ReelMaker import ReelMaker

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


def main():
    args = parse_arguments()

    os.chdir(args.workdir)

    setup_logger(args.loglevel)
    logging.info(f"Workdir is '{args.workdir}'")

    images = evaluate_images(args.images)

    imageScaler = ImageScaler(images, use_already_scaled_images=args.use_already_scaled_images)
    scaled_images = imageScaler.run()

    beatEvaluator = BeatEvaluator(args.audio)
    beat_times = beatEvaluator.run()
    # beat_times = BeatEvaluator.evaluate_beat_times_from_bpm(bpm = 140.09, total_duration = 7.9)

    durations = BeatEvaluator.eval_durations_from_beat_times(beat_times)

    reelMaker = ReelMaker(images=scaled_images, durations=durations,
                          audio_file_name=args.audio)
    reelMaker.run()


def evaluate_images(arg_images):
    if arg_images.endswith(".txt"):
        dir_text_file = os.path.dirname(arg_images)
        with open(arg_images, "r") as fin:
            lines = [line.rstrip() for line in fin]
            images = []
            for line in lines:
                if os.path.isabs(line):
                    images.append(line)
                else:
                    images.append(os.path.join(dir_text_file, line))
    else:
        images = arg_images.split(",")

    logging.info(f"{len(images)} images serve as input for the reel.")
    for index, image in enumerate(images):
        logging.debug(f"Image #{index+1}: {image}")

    return images


def parse_arguments():
    description = "A tool to create videos ('reels') based on a set of images and an audio file. " \
                  "From the audio file, the rhythm is automatically processed, " \
                  "so that the images are displayed according to the beat. " \
                  "Alternatively, the bpm / duration of the song can be specified."
    parser = argparse.ArgumentParser(prog="ReelMaker", description=description)

    #  ToDo also handle alread scaled images
    parser.add_argument("-i", "--images", type=str, required=True,
                        help="Comma-separated list of the unscaled (!) images, or alternatively the name of a "
                             "*.txt-File that contains the filenames (separated by newline). "
                             "Can be abspaths or relpaths to the workdir.")

    parser.add_argument("-a", "--audio", type=str, required=False,
                        help="Name of the audiofile. Can be an abspath or a relpath to the workdir. "
                             "If no audiofile is specified, the bpm / duration of the song "
                             "need to be specified by the other arguments.")  # ToDo: implement bpm / duration argument

    parser.add_argument("-w", "--workdir", type=str, default=os.getcwd(),
                        help="The working directory where the output files are stored. "
                             "If the input-files are passed as relpaths, the workdir serves as root. "
                             "If not specified, the current python working directory is used ('os.getcwd()').")

    parser.add_argument("-l", "--loglevel", choices=LOG_LEVELS, default=LOG_LEVEL_INFO,
                        help="Specify what log-messages shall be written.")

    parser.add_argument("-uasi", "--use_already_scaled_images", type=bool, default=False,
                        help="Set true, if the images have already been scaled and those scaled images "
                             "shall be re-used in order to skip the scaling-process.")

    args = parser.parse_args()
    return args


if __name__ == '__main__':
    main()