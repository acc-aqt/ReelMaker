import logging
import os
from itertools import cycle, islice
from moviepy import editor as mpe


from helpers import remove_file
from filename_helpers import is_image, is_video, get_lower_case_file_suffix, get_versioned_file_path


class ReelMaker:
    VIDEO_EXTENSION = ".mp4"  # reels work best with mp4
    FRAMES_PER_SECOND = 100

    def __init__(self, visuals, durations, audio_file_name="", base_name="reel"):
        self.visuals = visuals
        self.durations = durations
        self.audio_file_name = audio_file_name

        if self.audio_file_name:
            audio_base_name = os.path.basename(self.audio_file_name).split('.')[0]
            self.reel_name = get_versioned_file_path(base_name + "_" + audio_base_name + self.VIDEO_EXTENSION)
        else:
            self.reel_name = get_versioned_file_path(base_name + self.VIDEO_EXTENSION)

    def run(self):
        self.__stack_visuals_to_video()

        if self.audio_file_name:
            self.__add_audio_to_video()

    def __stack_visuals_to_video(self):
        logging.info("Stack visuals to make video (without audio)...")

        clips = []

        # repeat list of visuals until all durations are used
        visuals_to_stack = list(islice(cycle(self.visuals), len(self.durations)))
        for i, duration in enumerate(self.durations):
            visual = visuals_to_stack[i]
            if is_image(visual):
                image_clip = mpe.ImageClip(visual).set_duration(duration)
                clips.append(image_clip)
                image_clip.close()
            elif is_video(visual):
                clip_to_add = mpe.VideoFileClip(visual)
                start_time = 0  # ToDo: pass start_time per clip as input?
                clip_to_add = clip_to_add.subclip(start_time, start_time + duration)
                clips.append(clip_to_add)
                clip_to_add.close()
            else:
                file_suffix = get_lower_case_file_suffix(visual)
                raise IOError(f"Stacking not implemented for files of type '{file_suffix}'. "
                              f"File {visual} cannot be added to reel!")

        video = mpe.concatenate_videoclips(clips)  # method = "compose" ?
        video.write_videofile(self.reel_name, fps=60)  # ToDo: what fps to use?

        logging.info(f"Released video (without audio) --> {self.reel_name}")

    def __add_audio_to_video(self):
        logging.info("About to add audio...")

        temp_file_no_audio = "temp_reel_no_audio" + self.VIDEO_EXTENSION
        remove_file(temp_file_no_audio)

        os.rename(self.reel_name, temp_file_no_audio)

        videoclip = mpe.VideoFileClip(temp_file_no_audio)
        audioclip = mpe.AudioFileClip(self.audio_file_name)

        total_duration = min(videoclip.duration,
                             audioclip.duration)

        logging.debug(f"Video-Duration: {videoclip.duration}; Audio Duration: {audioclip.duration} "
                      f"--> crop both to {total_duration}")

        audioclip = audioclip.subclip(0, total_duration)
        videoclip = videoclip.subclip(0, total_duration)

        videoclip_with_audio = videoclip.set_audio(audioclip)
        videoclip_with_audio.write_videofile(self.reel_name)

        logging.info(f"Wrote file with audio --> {self.reel_name}")

        audioclip.close()
        videoclip.close()
        videoclip_with_audio.close()

        remove_file(temp_file_no_audio)

        logging.debug(f"Closed clips and remove temp-file '{temp_file_no_audio}'")


