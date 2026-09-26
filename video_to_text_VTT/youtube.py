"""Optional helper: download a YouTube (or any yt-dlp-supported) URL as audio.

Only imported when a URL is actually passed in, so `yt-dlp` stays an optional
extra for people who just want local-file transcription.
"""
from __future__ import annotations

import tempfile
from pathlib import Path


def looks_like_url(value: str) -> bool:
    return value.startswith("http://") or value.startswith("https://")


def download_audio(url: str) -> Path:
    try:
        import yt_dlp
    except ImportError as exc:  # pragma: no cover
        raise RuntimeError(
            "YouTube/URL input requires the optional 'yt-dlp' dependency. "
            "Install it with: pip install video-to-text-vtt[youtube]"
        ) from exc

    out_dir = Path(tempfile.mkdtemp())
    out_template = str(out_dir / "%(id)s.%(ext)s")

    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": out_template,
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "wav",
                "preferredquality": "192",
            }
        ],
        "quiet": True,
        "noprogress": True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        video_id = info["id"]

    downloaded = list(out_dir.glob(f"{video_id}.*"))
    if not downloaded:
        raise RuntimeError("yt-dlp finished but no output file was found.")
    return downloaded[0]
