# video_to_text_VTT

Extract speech from a video (or audio) file and generate **real, timestamped
WebVTT/SRT subtitles** — or plain text if that's all you want.

## What's new in v2.0.0

- 🧠 **Whisper-powered** (via `faster-whisper`) instead of the old Google Web
  Speech API wrapper: runs **offline**, supports ~100 languages, and is far
  more accurate — especially for non-English audio.
- 🎬 **Actually produces `.vtt` / `.srt` files** with real timestamps (v1 only
  ever wrote a single blob of plain text, despite the name).
- 📁 **Batch mode**: point it at a folder and it transcribes every video/audio
  file inside.
- ▶️ **YouTube/URL input**: pass a URL and it downloads + transcribes it
  (needs the optional `yt-dlp` extra).
- 🖥️ CPU or GPU (`--device cpu|cuda|auto`).

## Installation

### From PyPI
```bash
pip install video-to-text-vtt
# optional, for YouTube/URL input:
pip install "video-to-text-vtt[youtube]"
```
Then run as: `vtt_run [OPTIONS] path/to/YourVideo` or `python -m video_to_text_VTT [OPTIONS] path/to/YourVideo`

### With poetry
```bash
git clone https://github.com/momalekiii/VTT.git
cd VTT
poetry install
poetry run vtt_run [OPTIONS] path/to/YourVideo
```

### With pip locally
```bash
git clone https://github.com/momalekiii/VTT.git
cd VTT
pip install -r requirements.txt
python main.py [OPTIONS] path/to/YourVideo
```

## Usage

```bash
# Single video -> subtitles.vtt (auto-detected language)
vtt_run my_video.mp4

# Force language, write srt instead
vtt_run my_video.mp4 -lang fa --format srt

# Bigger/more accurate model, on GPU
vtt_run my_video.mp4 --model medium --device cuda

# Only transcribe a slice of the file
vtt_run my_video.mp4 --offset 30 --duration 60

# Whole folder, batch mode, all formats, into an output directory
vtt_run ./my_videos --format all -o ./subtitles

# Straight from a YouTube link
vtt_run "https://youtube.com/watch?v=..." --format vtt
```

### Options
- `--duration FLOAT` — audio length to transcribe, in seconds
- `--offset FLOAT` — how far from the start to begin, in seconds
- `-lang, --language TEXT` — language code (e.g. `en`, `fa`, `es`); omit to auto-detect
- `--model [tiny|base|small|medium|large-v3]` — Whisper model size (accuracy vs. speed)
- `--device [auto|cpu|cuda]`
- `-o, --output TEXT` — output file (single input) or output directory (folder/batch input)
- `--format [vtt|srt|txt|all]`
- `--help` — show this message and exit

## Migrating from v1

The CLI is backward-compatible for the common case (`python main.py path/to/video`),
but the default output is now a real `.vtt` file instead of a `.txt` file. Pass
`--format txt` if you want the old plain-text behavior.

## About
Extract Speech/Text from Video — now with real subtitles, offline Whisper
transcription, batch processing, and YouTube support.

### Topics
python, python3, speech-recognition, whisper, video-to-text, subtitles, vtt, srt
