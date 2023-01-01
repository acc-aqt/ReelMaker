import contextlib
import logging
import math
import os
import wave

import librosa
import numpy as np
from IPython import display as ipd

from WavConverter import WavConverter
from helpers import remove_file


class BeatEvaluator:

    @staticmethod
    def evaluate_beat_times_from_audio_file(path_to_audio_file):

        path_to_temp_wav = BeatEvaluator.__get_path_to_temp_wav(path_to_audio_file)
        WavConverter.convert(path_to_audio_file, path_to_temp_wav)
        beat_times = BeatEvaluator.__evaluate_beat_times_from_wav(path_to_temp_wav)
        remove_file(path_to_temp_wav)

        return beat_times

    @staticmethod
    def evaluate_beat_times_from_bpm(bpm, length):
        logging.info(f"Evaluate beat times by bpm ({bpm}) and length ({length}s)")
        bps = bpm / 60
        single_duration = 1 / bps
        number_of_beats = math.floor(length / single_duration)
        beat_times = []
        for i in range(1, 1 + number_of_beats):
            beat_times.append(i * single_duration)
        logging.info(f"Evaluated {len(beat_times)} beat times: {beat_times}")
        return beat_times

    @staticmethod
    def evaluate_durations_from_beat_times(beat_times):
        durations = []
        for index in range(len(beat_times)):
            if index == 0:
                durations.append(beat_times[0])
            else:
                durations.append(beat_times[index] - beat_times[index - 1])

        logging.info(f"Durations ({len(durations)}): {durations}")
        logging.info(f"Total duration: {sum(durations)}")
        return durations

    @staticmethod
    def __get_path_to_temp_wav(path_to_audio_file):
        workdir = os.path.dirname(path_to_audio_file)
        basename = os.path.splitext(os.path.basename(path_to_audio_file))[0]
        temp_wav_file = "TEMP_" + basename + ".wav"
        path_to_temp_wav_file = os.path.join(workdir, temp_wav_file)
        return path_to_temp_wav_file

    @staticmethod
    def __evaluate_beat_times_from_wav(wav_file):
        # from https://www.analyticsvidhya.com/blog/2018/02/audio-beat-tracking-for-music-information-retrieval/

        logging.info("Evaluate beat times from .wav...")

        x, sr = librosa.load(wav_file)  # only works with .wav...
        ipd.Audio(x, rate=sr)
        tempo, beat_times = librosa.beat.beat_track(x, sr=sr, start_bpm=120, units='time')

        # append total duration as last beat in order to use whole length of audio
        duration = BeatEvaluator.__get_total_duration_from_wav(wav_file)
        beat_times = np.append(beat_times, duration)

        logging.info(f"Evaluated {len(beat_times)} beat times from .wav: {beat_times}")
        return beat_times

    @staticmethod
    def __get_total_duration_from_wav(wav_file):
        with contextlib.closing(wave.open(wav_file, 'r')) as f:
            frames = f.getnframes()
            rate = f.getframerate()
            duration = frames / float(rate)
        return duration
