# ReelMaker
A tool that builds instagram wheels from an audio-input and a set of images.

## Usage

Call `main.py` with `-h` / `--help` flag to get info about the ReelMaker's usage and arguments.

```
python ReelMaker/src/main.py --help

usage: ReelMaker [-h] -v VISUALS [-a AUDIO] [-bpm BEATS_PER_MINUTE]
                 [-len LENGTH] [-w WORKDIR] [-log {INFO,DEBUG}]
                 [-uasv USE_ALREADY_SCALED_VISUALS]

A tool to create videos/reels based on a set of visuals (images and videos)
and an audio file. From the audio file, the rhythm is automatically processed,
so that the visuals are displayed according to the beat. Alternatively, the
bpm / duration of the song can be specified.

required arguments:
  -v VISUALS, --visuals VISUALS
                        Comma-separated list of the unscaled (!) visuals, or
                        alternatively the name of a *.txt-File that contains
                        the filenames (separated by newline). Can be abspaths
                        or relpaths to the workdir.

optional arguments:
  -a AUDIO, --audio AUDIO
                        Name of the audio-file. Can be an abspath or a relpath
                        to the workdir. If no audio-file is specified, the bpm
                        / length of the song/reel must be specified by the
                        other arguments.
  -bpm BEATS_PER_MINUTE, --beats_per_minute BEATS_PER_MINUTE
                        If no audio-file is specified, the beats per minute of
                        the song/reel must be specified.
  -len LENGTH, --length LENGTH
                        If no audio-file is specified, the length of the
                        song/reel must be specified (in seconds).
  -w WORKDIR, --workdir WORKDIR
                        The working directory where the output files are
                        stored. If the input-files are passed as relpaths, the
                        workdir serves as root. If not specified, the current
                        python working directory is used ('os.getcwd()').
  -log {INFO,DEBUG}, --loglevel {INFO,DEBUG}
                        Specify what log-messages shall be written.
  -uasv USE_ALREADY_SCALED_VISUALS, --use_already_scaled_visuals USE_ALREADY_SCALED_VISUALS
                        Set true, if the visuals have already been scaled and
                        those scaled visuals shall be re-used in order to skip
                        the scaling-process.
  ```
