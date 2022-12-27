import os

import librosa
from IPython import display as ipd
from moviepy import editor as mpe
from pydub import AudioSegment


class BeatEvaluator:

    def __init__(self, path_to_audio_file):

        self.path_to_input_file = path_to_audio_file

        self.__workdir = os.path.dirname(self.path_to_input_file)

        basename = os.path.splitext(os.path.basename(self.path_to_input_file))[0]
        self.__temp_wav_file = "TEMP_" + basename + ".wav"

        self.__path_to_temp_wav_file = os.path.join(self.__workdir, self.__temp_wav_file)

    def run(self):
        self.__remove_temp_wav()
        self.__create_temp_wav()
        beat_times = self.__evaluate_beat_times_from_wav()
        return beat_times

    def __evaluate_beat_times_from_wav(self):
        x, sr = librosa.load(self.__path_to_temp_wav_file)  # only works with .wav...
        # x, sr = librosa.load(path_to_audio_file)  # only works with .wav...
        ipd.Audio(x, rate=sr)
        tempo, beat_times = librosa.beat.beat_track(x, sr=sr, start_bpm=120, units='time')
        # clicks = librosa.clicks(beat_times, sr=sr, length=len(x))
        # ipd.Audio(x + clicks, rate=sr)
        return beat_times

    def __create_temp_wav(self):
        print(f"about to convert {self.path_to_input_file} to {self.__path_to_temp_wav_file}..")

        if self.path_to_input_file.endswith(".wav"):
            print("Audio file is .wav, so copy it to tempdir...")
            raise NotImplementedError("Must be implemented")
        elif self.path_to_input_file.endswith(".mp4"):
            print("Extract audio from video to wav for beat evaluation....")
            my_clip = mpe.VideoFileClip(self.path_to_input_file)  # r"downloaded_reel.mp4"
            my_clip.audio.write_audiofile(self.__path_to_temp_wav_file)
            print("Converted .mp4 to .wav")
        elif self.path_to_input_file.endswith(".mp3"):
            # ToDo: not sure if this works already...
            sound = AudioSegment.from_mp3(self.path_to_input_file)
            sound.export(self.__path_to_temp_wav_file, format="wav")
            print("Converted .mp3 to .wav")
        else:
            raise NotImplementedError(f"Filetype of {self.path_to_input_file} not supported for beat time evaluation")

    def __remove_temp_wav(self):
        if os.path.isfile(self.__path_to_temp_wav_file):
            os.remove(self.__path_to_temp_wav_file)
            print(f"Removed temp file {self.__path_to_temp_wav_file}")

    @staticmethod
    def eval_durations_from_beat_times(beat_times):
        beat_times = [0] + beat_times
        durations = [beat_times[n] - beat_times[n - 1] for n in range(1, len(beat_times))]
        return durations
