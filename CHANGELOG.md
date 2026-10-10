# Changelog

## v2.0.2 — Chrome Extension ("Online Subtitles")

### New Features
- Added **VTT Chrome Extension** (`chrome-extension/` & `vtt-chrome-extension.zip`):
  - Minimal online subtitle overlay for YouTube and any `<video>` playing in Chrome.
  - Main languages: **Persian (`FA`)**, **English (`EN`)**, and **Bilingual (`FA + EN`)**.
  - Sentence-paced reading buffer that merges rapid word-by-word captions into calm 3.5s–5.5s sentences.
  - Subtle faded top-right corner language switcher chip on video hover.
  - Live audio speech recognition fallback (`🎤`) and 1-click `.vtt` / `.srt` export.
- Updated landing page (`index.html`) with live interactive extension demo and direct free `.zip` download.

## v2.0.0 — "Awakens"

### Breaking / core changes
- Replaced `SpeechRecognition` (Google Web Speech API, online-only) with
  **Whisper** via `faster-whisper` — offline, ~100 languages, far more accurate.
- Default output is now a real **`.vtt` file with timestamps**, not raw `.txt`.
  Use `--format txt` to keep the old plain-text behavior.
- `moviepy` bumped from `~1.0.3` to `~2.1.1` (audio extraction API updated
  accordingly — `subclipped` instead of the removed `subclip`, guarded for
  compatibility).

### New features
- `--format {vtt,srt,txt,all}` — choose subtitle format(s).
- `--model {tiny,base,small,medium,large-v3}` — trade off speed vs. accuracy.
- `--device {auto,cpu,cuda}` — GPU support.
- Batch mode: pass a folder as `PATH` and every video/audio file inside gets
  transcribed.
- YouTube/URL input: pass a URL as `PATH` (requires the optional
  `video-to-text-vtt[youtube]` extra).

### Infra
- Added unit tests for subtitle formatting/timestamp logic.
- Added GitHub Actions CI.
