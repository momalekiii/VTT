# Developed by Momalekiii
# Used libraries in this code are <--SpeechRecognition 3.8.1 & MoviePy 1.0.3-->
# follow me on all Social media as : @momalekiii


# Create a folder and put your video file and VTT.py

from __future__ import annotations

import logging
import sys
from pathlib import Path

import click
import speech_recognition
from moviepy import editor

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

AUDIO_FILE = "converted.wav"
RESULT_FILE = "recognized.txt"


def extract_audio_from_movie(movie_file: str) -> None:
    try:
        clip = editor.VideoFileClip(movie_file)
    except OSError as e:
        logging.error(
            f"MoviePy failed to read the duration of file {movie_file} (Maybe not a video file?)"
        )
        sys.exit()
    logging.info("Please wait until the audio extraction is finished")
    clip.audio.write_audiofile(AUDIO_FILE)


def get_text_from_audio(
    duration: float | None = None, offset: float | None = None, language: str = "en-US"
) -> str:
    recognizer = speech_recognition.Recognizer()
    with speech_recognition.AudioFile(AUDIO_FILE) as source:
        audio_data = recognizer.record(source, duration=duration, offset=offset)
    logging.info("converting audio to text. This may take some time")
    try:
        text_result: str = recognizer.recognize_google(audio_data, language=language)
    except speech_recognition.RequestError as e:
        logging.error(
            f"{repr(e)}. Maybe the audio is too long."
            " Consider tweeking --duration, --offset, and/or --language option(s)"
        )
        sys.exit()
    except speech_recognition.UnknownValueError as e:
        logging.error(
            f"{repr(e)}. Maybe the audio is not recognized."
            " Consider tweeking --duration, --offset, and/or --language option(s)"
        )
        sys.exit()
    return text_result


def export_result(text_result: str, output: str) -> None:
    with open(output, mode="w") as file:
        file.write("Recognized Speech:\n")
        file.write(text_result)
    logging.info(f"Done! Check {output} to see the results")


@click.command("video-to-text-VVT command line")
@click.argument("movie_file")
@click.option("--duration", type=float, help="Audio length [seconds]")
@click.option("--offset", type=float, help="How far from zero you start [seconds]")
@click.option(
    "--language",
    "-lang",
    default="en-US",
    help="Audio language. Supported languages can be found in <http://stackoverflow.com/a/14302134>",
)
@click.option("--output", "-o", default=RESULT_FILE, help="The result file")
def main(
    movie_file: str,
    duration: float | None = None,
    offset: float | None = None,
    language: str = "en-US",
    output: str = RESULT_FILE,
) -> None:
    if not Path(movie_file).exists():
        logging.error("File does not exist")
        return
    extract_audio_from_movie(movie_file)
    text_result = get_text_from_audio(duration, offset, language)
    export_result(text_result, output)


if __name__ == "__main__":
    main()
