import logging
import shutil

from moviepy import editor as mpe
# ffprobe or are avprobe required for mp3 conversion, see https://deviloper.in/mp3-to-wav-file-conversion-using-python
from pydub import AudioSegment

from filename_helpers import get_lower_case_file_suffix
from helpers import remove_file

WAV_SUFFIX = "wav"
MP3_SUFFIX = "mp3"
MP4_SUFFIX = "mp4"

SUPPORTED_INPUTS = [MP3_SUFFIX, MP4_SUFFIX]


class WavConverter:

    @staticmethod
    def convert(input_file, output_file):
        if get_lower_case_file_suffix(output_file) != WAV_SUFFIX:
            raise IOError(f"Invalid name for output file '{output_file}'. Must have suffix '{WAV_SUFFIX}'. ")

        remove_file(output_file)

        logging.info(f"About to convert {input_file} to {output_file}...")

        if get_lower_case_file_suffix(input_file) == WAV_SUFFIX:
            shutil.copyfile(input_file, output_file)
            logging.info("Input is .wav, so just copied it.")
            return

        if get_lower_case_file_suffix(input_file) == "mp4":
            WavConverter.__convert_from_mp4(input_file, output_file)
        elif get_lower_case_file_suffix(input_file) == "mp3":
            WavConverter.__convert_from_mp3(input_file, output_file)
        else:
            raise IOError(f"Filetype of {input} not supported for conversion to {WAV_SUFFIX}. "
                          f"File must be of type {'/'.join(SUPPORTED_INPUTS)}.")

        logging.info("Finished conversion!")

    @staticmethod
    def __convert_from_mp3(input_file, output_file):
        sound = AudioSegment.from_mp3(input_file)
        sound.export(output_file, format="wav")

    @staticmethod
    def __convert_from_mp4(input_file, output_file):
        my_clip = mpe.VideoFileClip(input_file)
        my_clip.audio.write_audiofile(output_file)
