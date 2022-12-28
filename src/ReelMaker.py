import os
from itertools import cycle, islice

import cv2
from moviepy import editor as mpe


class ReelMaker:
    VIDEO_EXTENSION = ".mp4"  # reels work best with mp4
    FRAMES_PER_SECOND = 100

    def __init__(self, working_dir, scaled_images, durations, audio_file_name="", base_name="reel"):
        self.working_dir = working_dir
        self.video_base_name = base_name
        self.scaled_images = scaled_images
        self.durations = durations
        self.audio_file_name = audio_file_name

        audio_file_base_name = self.audio_file_name.split(".")[0]
        self.filename_video_without_audio = self.video_base_name + "_TEMP_NO_AUDIO_" + audio_file_base_name + self.VIDEO_EXTENSION
        self.filename_video_with_audio = self.video_base_name + "_WITH_AUDIO_" + audio_file_base_name + self.VIDEO_EXTENSION

    def run(self):
        self.__stack_images_to_video()


        if self.audio_file_name:
            print("About to add audio...")
            self.__add_audio_to_video()
            print("Added audio!")

    def __stack_images_to_video(self):
        print("Stack images to make video (without audio)...")

        path_to_video_without_audio = os.path.join(self.working_dir, self.filename_video_without_audio)

        if os.path.isfile(path_to_video_without_audio):
            os.remove(path_to_video_without_audio)
            print(f"Removed file {path_to_video_without_audio}")

        frame = cv2.imread(os.path.join(self.working_dir, self.scaled_images[0]))
        height, width, _ = frame.shape

        fourcc = cv2.VideoWriter_fourcc(*'MP4V')  # only mp4 seems to works

        video = cv2.VideoWriter(os.path.join(self.working_dir, self.filename_video_without_audio), fourcc,
                                self.FRAMES_PER_SECOND,
                                (width, height))

        counter = 0
        looped_scaled_images = list(islice(cycle(self.scaled_images), len(self.durations)))
        for duration in self.durations:
            print(f"Stack image {counter +1} / {len(self.durations)}...")
            frames = int(duration * self.FRAMES_PER_SECOND)
            for frame in range(frames):
                video.write(cv2.imread(os.path.join(self.working_dir, looped_scaled_images[counter])))
            counter += 1


        print("Finished stacking!")
        cv2.destroyAllWindows()
        video.release()
        print("Released video (without audio)...")

    def __add_audio_to_video(self):

        path_to_video_with_audio = os.path.join(self.working_dir, self.filename_video_with_audio)

        if os.path.isfile(path_to_video_with_audio):
            os.remove(path_to_video_with_audio)
            print(f"Removed file {path_to_video_with_audio}")

        videoclip = mpe.VideoFileClip(os.path.join(self.working_dir, self.filename_video_without_audio))
        audioclip = mpe.AudioFileClip(os.path.join(self.working_dir, self.audio_file_name))

        total_duration = min(videoclip.duration,
                             audioclip.duration)
        print(f"Video-Duration: {videoclip.duration}; "
              f"Audio Duration: {audioclip.duration} "
              f"--> crop both to {total_duration}")

        audioclip = audioclip.subclip(0, total_duration)
        videoclip = videoclip.subclip(0, total_duration)

        videoclip_with_audio = videoclip.set_audio(audioclip)
        videoclip_with_audio.write_videofile(os.path.join(self.working_dir, path_to_video_with_audio))

        audioclip.close()
        videoclip.close()
        videoclip_with_audio.close()

        print(f"Wrote file {path_to_video_with_audio}")
