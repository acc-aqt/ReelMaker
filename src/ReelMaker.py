import logging
import os
from itertools import cycle, islice

import cv2
from moviepy import editor as mpe


class ReelMaker:
    VIDEO_EXTENSION = ".mp4"  # reels work best with mp4
    FRAMES_PER_SECOND = 100

    def __init__(self, images, durations, audio_file_name="", base_name="reel"):
        self.images = images
        self.durations = durations
        self.audio_file_name = audio_file_name

        audio_file_base_name = self.audio_file_name.split(".")[0]
        self.video_without_audio = base_name + "_TEMP_NO_AUDIO_" + audio_file_base_name + self.VIDEO_EXTENSION
        self.video_with_audio = base_name + "_WITH_AUDIO_" + audio_file_base_name + self.VIDEO_EXTENSION

    def run(self):
        self.__stack_images_to_video()

        if self.audio_file_name:
            self.__add_audio_to_video()

    def __stack_images_to_video(self):
        if os.path.isfile(self.video_without_audio):
            os.remove(self.video_without_audio)
            logging.debug(f"Removed file {self.video_without_audio}")

        logging.info("Stack images to make video (without audio)...")

        height, width = self.get_height_width()

        fourcc = cv2.VideoWriter_fourcc(*'MP4V')  # only mp4 seems to works

        video = cv2.VideoWriter(self.video_without_audio, fourcc, self.FRAMES_PER_SECOND, (width, height))

        images_to_stack = list(islice(cycle(self.images), len(self.durations))) # repeat list of images until all durations are used
        for i, duration in enumerate(self.durations):
            logging.debug(f"Stack image {i +1} / {len(self.durations)}...")
            frames = int(duration * self.FRAMES_PER_SECOND)
            for frame in range(frames):
                video.write(cv2.imread(images_to_stack[i]))

        logging.debug("Finished stacking!")
        cv2.destroyAllWindows()
        video.release()
        logging.info(f"Released video (without audio) --> {self.video_without_audio}")

    def get_height_width(self):
        frame = cv2.imread(self.images[0])
        height, width, _ = frame.shape
        return height, width

    def __add_audio_to_video(self):
        logging.info("About to add audio...")

        if os.path.isfile(self.video_with_audio):
            os.remove(self.video_with_audio)
            logging.debug(f"Removed file {self.video_with_audio}")

        videoclip = mpe.VideoFileClip(self.video_without_audio)
        audioclip = mpe.AudioFileClip( self.audio_file_name)

        total_duration = min(videoclip.duration,
                             audioclip.duration)
        logging.debug(f"Video-Duration: {videoclip.duration}; Audio Duration: {audioclip.duration} "
                      f"--> crop both to {total_duration}")

        audioclip = audioclip.subclip(0, total_duration)
        videoclip = videoclip.subclip(0, total_duration)

        videoclip_with_audio = videoclip.set_audio(audioclip)
        videoclip_with_audio.write_videofile(self.video_with_audio)

        audioclip.close()
        videoclip.close()
        videoclip_with_audio.close()

        logging.info(f"Wrote file with audio --> {self.video_with_audio}")
