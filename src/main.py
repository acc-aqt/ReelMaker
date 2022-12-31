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


def setup_logger(loglevel):
    now_string = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    logfile = f'make_reel_{now_string}.log'
    logging.basicConfig(filename=logfile, level=loglevel)
    logging.getLogger().addHandler(logging.StreamHandler(sys.stdout))


def main():
    args = parse_arguments()

    workdir = args.workdir

    audio_file = args.audio
    images = args.images.split(",")
    loglevel = args.loglevel
    use_already_scaled_images = args.use_already_scaled_images

    os.chdir(workdir)

    setup_logger(loglevel)

    logging.info(f"Workdir is '{workdir}'")

    imageScaler = ImageScaler(images, use_already_scaled_images=use_already_scaled_images)
    scaled_images = imageScaler.run()
    beatEvaluator = BeatEvaluator(audio_file)
    beat_times = beatEvaluator.run()
    # beat_times = BeatEvaluator.evaluate_beat_times_from_bpm(bpm = 140.09, total_duration = 7.9)

    # ToDo bugfix: Evaluated 4 beat times from .wav: [3.76163265 4.69043084 5.54956916 6.40870748]
    # --> Durations(3): [0.9287981859410435, 0.8591383219954647, 0.8591383219954647]

    durations = BeatEvaluator.eval_durations_from_beat_times(beat_times)
    reelMaker = ReelMaker(images=scaled_images, durations=durations,
                          audio_file_name=audio_file)
    reelMaker.run()


def parse_arguments():
    description = "A tool to create videos ('reels') based on a set of images and an audio file. " \
                  "From the audio file, the rhythm is automatically processed, " \
                  "so that the images are displayed according to the beat. " \
                  "Alternatively, the bpm / duration of the song can be specified."
    parser = argparse.ArgumentParser(prog="ReelMaker", description=description)

    #  ToDo also handle alread scaled images
    parser.add_argument("-i", "--images", type=str, required=True,
                        help="Comma-separated list of the unscaled (!) images (relative to the workdir) "
                             "that shall be stacked to build the reel.")  # ToDo: pass in file

    parser.add_argument("-a", "--audio", type=str, required=False,
                        help="Name of the audiofile. If no audiofile is specified, the bpm / duration of the song "
                             "need to be specified by the other arguments.")  # ToDo: implement bpm / duration argument

    parser.add_argument("-w", "--workdir", type=str, default=os.getcwd(),
                        help="The working directory where all input and output files are stored. "
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