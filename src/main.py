import os

from BeatEvaluator import BeatEvaluator
from ImageScaler import ImageScaler
from ReelMaker import ReelMaker

WORK_DIR = r"C:\path\to\workdir"  # all inputs files must be in  workdir. all outputs will be written there as well...

AUDIO_FILE_NAME = 'file_with_audio.mp4'  # can be an mp3, wav, or mp4

UNSCALED_IMAGES = ["list.jpg", "of.jpg", "images.jpg"]


def main():
    imageScaler = ImageScaler(UNSCALED_IMAGES, WORK_DIR, images_are_already_scaled=True)
    scaled_images = imageScaler.run()

    print(f"Number of scaled images: {len(scaled_images)}")

    beatEvaluator = BeatEvaluator(os.path.join(WORK_DIR, AUDIO_FILE_NAME))
    beat_times = beatEvaluator.run()
    durations = beatEvaluator.eval_durations_from_beat_times(beat_times)

    print(f"Beat-times ({len(beat_times)}): {beat_times}")
    print(f"Durations ({len(durations)}): {durations}")

    reelMaker = ReelMaker(working_dir = WORK_DIR, scaled_images=scaled_images, durations=durations, audio_file_name=AUDIO_FILE_NAME)
    reelMaker.run()


if __name__ == '__main__':
    main()
