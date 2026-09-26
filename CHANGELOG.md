# Changelog

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
