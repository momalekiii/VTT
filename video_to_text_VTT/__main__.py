# Developed by Momalekiii
# Used libraries in this code are <--SpeechRecognition 3.8.1 & MoviePy 1.0.3-->
# follow me on all Social media as : @momalekiii


# Create a folder and put your video file and VTT.py


import logging
import sys
from pathlib import Path

import speech_recognition
from moviepy import editor

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

AUDIO_FILE = "converted.wav"
RESULT_FILE = "recognized.txt"


def get_movie_file() -> str:
    try:
        movie_file = sys.argv[1]  # % python VTT.py movie_file
    except IndexError:  # no file was provided in the terminal
        movie_file = input("Put the name of your video with the extention: ").strip()
    if not movie_file:
        logging.error("No file was entered")
        sys.exit()
    if not Path(movie_file).exists():
        logging.error("File does not exist")
        sys.exit()
    return movie_file


def extract_audio_from_movie(movie_file: str) -> None:
    try:
        clip = editor.VideoFileClip(movie_file)
    except OSError as e:
        logging.error(
            f"MoviePy failed to read the duration of file {movie_file} (Maybe not a video file?"
        )
        sys.exit()
        return
    clip.audio.write_audiofile(AUDIO_FILE)


def get_text_from_audio() -> str:
    recognizer = speech_recognition.Recognizer()
    with speech_recognition.AudioFile(AUDIO_FILE) as source:
        audio_data = recognizer.record(source)
    text_result: str = recognizer.recognize_google(audio_data)
    return text_result


def export_result(text_result: str) -> None:
    with open(RESULT_FILE, mode="w") as file:
        file.write("Recognized Speech:\n")
        file.write(text_result)
    logging.info(f"Done! Check {RESULT_FILE} to see the results")


def main() -> None:
    movie_file = get_movie_file()
    extract_audio_from_movie(movie_file)
    text_result = get_text_from_audio()
    export_result(text_result)


if __name__ == "__main__":
    main()
