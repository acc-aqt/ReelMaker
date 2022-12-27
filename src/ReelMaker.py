import os

import cv2
from moviepy import editor as mpe


class ReelMaker:
    VIDEO_EXTENSION = ".mp4"  # reels work best with mp4
    FRAMES_PER_SECOND = 100

    def __init__(self, working_dir):
        self.working_dir = working_dir
        self.video_base_name = None

    def add_images_to_video(self, video_base_name, scaled_images, durations):
        self.video_base_name = video_base_name

        filename_video_without_audio = self.video_base_name + self.VIDEO_EXTENSION
        path_to_video_without_audio = os.path.join(self.working_dir, filename_video_without_audio)

        if os.path.isfile(path_to_video_without_audio):
            os.remove(path_to_video_without_audio)
            print(f"Removed file {path_to_video_without_audio}")

        frame = cv2.imread(os.path.join(self.working_dir, scaled_images[0]))
        height, width, _ = frame.shape

        fourcc = cv2.VideoWriter_fourcc(*'MP4V')  # only mp4 seems to works

        video = cv2.VideoWriter(os.path.join(self.working_dir, filename_video_without_audio), fourcc,
                                self.FRAMES_PER_SECOND,
                                (width, height))
        counter = 0

        if len(scaled_images) > len(durations):
            scaled_images_sliced = scaled_images[:len(durations)]
            print(f"Scaled images now has length  {len(scaled_images_sliced)}")
        else:
            scaled_images_sliced = scaled_images

        for image in scaled_images_sliced:
            print(f"Stack image {counter +1} / {len(scaled_images_sliced)}...")
            frames = int(durations[counter] * self.FRAMES_PER_SECOND)
            for frame in range(frames):
                video.write(cv2.imread(os.path.join(self.working_dir, image)))
            counter += 1
        print("Finished stacking!")
        cv2.destroyAllWindows()
        video.release()
        print("Released video!")

    def add_audio_to_video(self, audio_file_name):
        audio_file_base_name = audio_file_name.split(".")[0]
        filename_video_with_audio = self.video_base_name + "_" + audio_file_base_name + self.VIDEO_EXTENSION
        path_to_video_with_audio = os.path.join(self.working_dir, filename_video_with_audio)
        filename_video_without_audio = self.video_base_name + self.VIDEO_EXTENSION  # ToDo: remove code duplication

        if os.path.isfile(path_to_video_with_audio):
            os.remove(path_to_video_with_audio)
            print(f"Removed file {path_to_video_with_audio}")

        videoclip = mpe.VideoFileClip(os.path.join(self.working_dir, filename_video_without_audio))
        audioclip = mpe.AudioFileClip(os.path.join(self.working_dir, audio_file_name))

        total_duration = min(videoclip.duration,
                             audioclip.duration)  # ToDo: alternativ: audio limitiert. iteriere so lange ueber die bilder als schleife, bis audio durch ist
        print(f"Video-Duration: {videoclip.duration}; "
              f"Audio Duration: {audioclip.duration} "
              f"--> crop both to {total_duration}")

        audioclip = audioclip.subclip(0, total_duration)
        videoclip = videoclip.subclip(0, total_duration)

        videoclip_with_audio = videoclip.set_audio(audioclip)
        videoclip_with_audio.write_videofile(os.path.join(self.working_dir, path_to_video_with_audio))

        print(f"Wrote file {path_to_video_with_audio}")
