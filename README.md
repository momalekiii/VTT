# VTT 2.0

Extract speech from a video (or audio) file and generate **real, timestamped
WebVTT/SRT subtitles** — or plain text if that's all you want.

# Release notes (Awakens 🐉")

VTT is finally awake after a long sleep — and it finally makes actual `.vtt`
files. 😄

## ✨ Highlights

- 🧠 **New brain**: swapped the old online-only Google Web Speech API for
  **Whisper** (via `faster-whisper`). Fully offline, ~100 languages, and much
  more accurate — especially for Persian/non-English audio.
- 🎬 **Real subtitles at last**: output is now genuine timestamped
  `.vtt` / `.srt`, not a single blob of plain text.
- 📁 **Batch mode**: point it at a folder, get subtitles for every video
  inside.
- ▶️ **YouTube/URL input**: `vtt_run "https://youtube.com/watch?v=..."` just
  works (needs the optional `[youtube]` extra).
- 🖥️ **GPU support**: `--device cuda` for faster runs.
- 🎚️ **Model size control**: `--model tiny|base|small|medium|large-v3` to
  trade off speed vs. accuracy.

## ⚠️ Breaking change
Default output is now `.vtt` instead of `.txt`. Pass `--format txt` if you
relied on the old plain-text output.

## 📦 Install
```bash
pip install video-to-text-vtt
pip install "video-to-text-vtt[youtube]"   # optional, for URL input
```

## 🔧 Example
```bash
vtt_run my_video.mp4 -lang fa --model medium
vtt_run ./my_videos --format all -o ./subtitles
```

## Migrating from v1

The CLI is backward-compatible for the common case (`python main.py path/to/video`),
but the default output is now a real `.vtt` file instead of a `.txt` file. Pass
`--format txt` if you want the old plain-text behavior.
