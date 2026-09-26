"""Transcription backend.

v2 replaces the old `SpeechRecognition` + Google Web Speech API call (which
needed an internet connection, was rate-limited, and did poorly outside
English) with faster-whisper: it runs fully offline, supports ~100 languages,
and returns real per-segment timestamps -- which is what finally lets this
project produce genuine .vtt/.srt subtitle files.
"""
from __future__ import annotations

from pathlib import Path
from typing import List, Optional

from .subtitle_writer import Segment

_MODEL_CACHE: dict = {}


def _get_model(model_size: str, device: str, compute_type: str):
    key = (model_size, device, compute_type)
    if key not in _MODEL_CACHE:
        from faster_whisper import WhisperModel

        _MODEL_CACHE[key] = WhisperModel(model_size, device=device, compute_type=compute_type)
    return _MODEL_CACHE[key]


def transcribe(
    audio_path: str | Path,
    *,
    model_size: str = "small",
    language: Optional[str] = None,
    device: str = "auto",
    compute_type: str = "int8",
) -> List[Segment]:
    """Transcribe an audio file and return a list of timestamped Segments.

    Parameters
    ----------
    model_size: tiny | base | small | medium | large-v3 (bigger = more accurate, slower)
    language: BCP-47-ish code like "en", "fa", "es". None = auto-detect.
    device: "cpu", "cuda", or "auto".
    compute_type: e.g. "int8" (fast, CPU-friendly) or "float16" (GPU).
    """
    model = _get_model(model_size, device, compute_type)
    raw_segments, _info = model.transcribe(
        str(audio_path),
        language=language,
        vad_filter=True,  # skip silence instead of hallucinating text on it
    )
    return [Segment(start=s.start, end=s.end, text=s.text) for s in raw_segments]
