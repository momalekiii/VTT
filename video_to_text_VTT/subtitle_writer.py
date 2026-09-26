"""Turn transcription segments into real WebVTT / SRT / plain-text files.

This is the module that finally makes "VTT" actually produce .vtt files with
timestamps, instead of a single blob of raw text.
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, List


@dataclass
class Segment:
    start: float  # seconds
    end: float    # seconds
    text: str


def _format_timestamp(seconds: float, *, comma: bool) -> str:
    if seconds < 0:
        seconds = 0.0
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    millis = int(round((seconds - int(seconds)) * 1000))
    if millis == 1000:  # rounding edge case
        millis = 0
        secs += 1
        if secs == 60:
            secs = 0
            minutes += 1
            if minutes == 60:
                minutes = 0
                hours += 1
    sep = "," if comma else "."
    return f"{hours:02d}:{minutes:02d}:{secs:02d}{sep}{millis:03d}"


def to_vtt_timestamp(seconds: float) -> str:
    return _format_timestamp(seconds, comma=False)


def to_srt_timestamp(seconds: float) -> str:
    return _format_timestamp(seconds, comma=True)


def write_vtt(segments: Iterable[Segment], output_path: str | Path) -> Path:
    output_path = Path(output_path)
    lines: List[str] = ["WEBVTT", ""]
    for seg in segments:
        lines.append(f"{to_vtt_timestamp(seg.start)} --> {to_vtt_timestamp(seg.end)}")
        lines.append(seg.text.strip())
        lines.append("")
    output_path.write_text("\n".join(lines), encoding="utf-8")
    return output_path


def write_srt(segments: Iterable[Segment], output_path: str | Path) -> Path:
    output_path = Path(output_path)
    lines: List[str] = []
    for i, seg in enumerate(segments, start=1):
        lines.append(str(i))
        lines.append(f"{to_srt_timestamp(seg.start)} --> {to_srt_timestamp(seg.end)}")
        lines.append(seg.text.strip())
        lines.append("")
    output_path.write_text("\n".join(lines), encoding="utf-8")
    return output_path


def write_txt(segments: Iterable[Segment], output_path: str | Path) -> Path:
    output_path = Path(output_path)
    text = " ".join(seg.text.strip() for seg in segments)
    output_path.write_text(text, encoding="utf-8")
    return output_path


WRITERS = {
    "vtt": write_vtt,
    "srt": write_srt,
    "txt": write_txt,
}
