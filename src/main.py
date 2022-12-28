import datetime
import logging
import os
import sys

from BeatEvaluator import BeatEvaluator
from ImageScaler import ImageScaler
from ReelMaker import ReelMaker

WORK_DIR = r"C:\path\to\workdir"  # all inputs files must be in  workdir. all outputs will be written there as well...

AUDIO_FILE_NAME = 'file_with_audio.mp4'  # can be an mp3, wav, or mp4

UNSCALED_IMAGES = ["list.jpg", "of.jpg", "images.jpg"]


def setup_logger():
    now_string = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    logfile = f'make_reel_{now_string}.log'
    logging.basicConfig(filename=os.path.join(WORK_DIR, logfile), level=logging.INFO)
    logging.getLogger().addHandler(logging.StreamHandler(sys.stdout))


def main():
    setup_logger()

    imageScaler = ImageScaler(UNSCALED_IMAGES, WORK_DIR, images_are_already_scaled=False)
    scaled_images = imageScaler.run()

    beatEvaluator = BeatEvaluator(os.path.join(WORK_DIR, AUDIO_FILE_NAME))
    beat_times = beatEvaluator.run()
    durations = beatEvaluator.eval_durations_from_beat_times(beat_times)

    reelMaker = ReelMaker(working_dir=WORK_DIR, scaled_images=scaled_images, durations=durations,
                          audio_file_name=AUDIO_FILE_NAME)
    reelMaker.run()


if __name__ == '__main__':
    main()
