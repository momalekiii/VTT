"""Extract a (possibly trimmed) audio track from a video file as a temp WAV file."""
from __future__ import annotations

import tempfile
from pathlib import Path
from typing import Optional

AUDIO_EXTENSIONS = {".wav", ".mp3", ".m4a", ".flac", ".ogg", ".aac"}


def is_audio_file(path: str | Path) -> bool:
    return Path(path).suffix.lower() in AUDIO_EXTENSIONS


def extract_audio(
    input_path: str | Path,
    *,
    offset: Optional[float] = None,
    duration: Optional[float] = None,
) -> Path:
    """Return a path to a 16kHz mono WAV file ready for Whisper.

    If `input_path` is already an audio file and no trimming is requested,
    it is used as-is (still fine for faster-whisper/ffmpeg to read most formats).
    """
    input_path = Path(input_path)

    if is_audio_file(input_path) and offset is None and duration is None:
        return input_path

    # Local import so the rest of the package works even if moviepy isn't
    # installed (e.g. when only transcribing pre-extracted audio).
    from moviepy import AudioFileClip, VideoFileClip  # moviepy >= 2.0

    tmp_wav = Path(tempfile.mkstemp(suffix=".wav")[1])

    if is_audio_file(input_path):
        clip = AudioFileClip(str(input_path))
    else:
        clip = VideoFileClip(str(input_path)).audio

    start = offset or 0
    end = (start + duration) if duration else None
    if start or end:
        clip = clip.subclipped(start, end) if hasattr(clip, "subclipped") else clip.subclip(start, end)

    clip.write_audiofile(str(tmp_wav), fps=16000, nbytes=2, codec="pcm_s16le", logger=None)
    clip.close()
    return tmp_wav
