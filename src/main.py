import argparse
import logging
import os

from BeatEvaluator import BeatEvaluator
from ReelMaker import ReelMaker
from VisualsScaler import VisualsScaler
from setup_logger import LOG_LEVEL_INFO, LOG_LEVELS, setup_logger


def main():
    args = parse_arguments()

    os.chdir(args.workdir)

    setup_logger(args.loglevel)
    logging.info(f"Workdir is '{args.workdir}'")

    visuals = evaluate_visuals(args.visuals)

    visualsScaler = VisualsScaler(visuals, use_already_scaled_visuals=args.use_already_scaled_visuals)
    scaled_visuals = visualsScaler.run()

    if args.beats_per_minute and args.length:
        beat_times = BeatEvaluator.evaluate_beat_times_from_bpm(bpm=args.beats_per_minute, length=args.length)
    else:
        beatEvaluator = BeatEvaluator(args.audio)
        beat_times = beatEvaluator.run()

    durations = BeatEvaluator.eval_durations_from_beat_times(beat_times)

    reelMaker = ReelMaker(visuals=scaled_visuals, durations=durations,
                          audio_file_name=args.audio)
    reelMaker.run()


def evaluate_visuals(arg_visuals):
    if arg_visuals.endswith(".txt"):  # evaluate visuals from text file
        dir_text_file = os.path.dirname(arg_visuals)
        with open(arg_visuals, "r") as fin:
            lines = [line.rstrip() for line in fin]
            visuals = []
            for line in lines:
                if os.path.isabs(line):
                    visuals.append(line)
                else:
                    visuals.append(os.path.join(dir_text_file, line))
    else:  # evaluate directly from passed input string. comma separated list.
        visuals = arg_visuals.split(",")

    logging.info(f"{len(visuals)} visuals serve as input for the reel.")
    for index, visual in enumerate(visuals):
        logging.debug(f"Visual #{index+1}: {visual}")

    return visuals


def parse_arguments():
    description = "A tool to create videos/reels based on a set of visuals (images and videos) and an audio file. " \
                  "From the audio file, the rhythm is automatically processed, " \
                  "so that the visuals are displayed according to the beat. " \
                  "Alternatively, the bpm / duration of the song can be specified."
    parser = argparse.ArgumentParser(prog="ReelMaker", description=description)
    parser._action_groups.pop()

    required = parser.add_argument_group('required arguments')
    optional = parser.add_argument_group('optional arguments')

    #  ToDo also handle alread scaled visuals
    required.add_argument("-v", "--visuals", type=str, required=True,
                          help="Comma-separated list of the unscaled (!) visuals, or alternatively the name of a "
                               "*.txt-File that contains the filenames (separated by newline). "
                               "Can be abspaths or relpaths to the workdir.")

    optional.add_argument("-a", "--audio", type=str, required=False,
                          help="Name of the audio-file. Can be an abspath or a relpath to the workdir. "
                               "If no audio-file is specified, the bpm / length of the song/reel "
                               "must be specified by the other arguments.")

    optional.add_argument("-bpm", "--beats_per_minute", type=float, required=False,
                          help="If no audio-file is specified, the beats per minute of the song/reel must be specified.")

    optional.add_argument("-len", "--length", type=float, required=False,
                          help="If no audio-file is specified, "
                               "the length of the song/reel must be specified (in seconds).")

    optional.add_argument("-w", "--workdir", type=str, default=os.getcwd(),
                          help="The working directory where the output files are stored. "
                               "If the input-files are passed as relpaths, the workdir serves as root. "
                               "If not specified, the current python working directory is used ('os.getcwd()').")

    optional.add_argument("-log", "--loglevel", choices=LOG_LEVELS, default=LOG_LEVEL_INFO,
                          help="Specify what log-messages shall be written.")

    optional.add_argument("-uasv", "--use_already_scaled_visuals", type=bool, default=False,
                          help="Set true, if the visuals have already been scaled and those scaled visuals "
                               "shall be re-used in order to skip the scaling-process.")

    args = parser.parse_args()

    if not args.audio and not (args.length and args.beats_per_minute):
        raise IOError("If no audio-file is specified, then both the beats-per-minute, "
                      "as well as the length of the song/reel need to be specified.")

    return args


if __name__ == '__main__':
    main()
