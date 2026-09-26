"""video_to_text_VTT — extract speech from video/audio and generate real WebVTT/SRT subtitles.

v2.0.0
- Whisper-based transcription (faster-whisper) instead of the old
  Google Web Speech API wrapper.
- Produces *actual* .vtt / .srt subtitle files with timestamps (not just raw .txt).
- Batch mode for whole folders.
- Optional YouTube URL input via yt-dlp.
"""

__version__ = "2.0.0"
