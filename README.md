# VTT 2.0.2

Extract speech from a video (or audio) file and generate **real, timestamped
WebVTT/SRT subtitles** — or use the **VTT Chrome Extension** for live online
**Persian (FA) & English (EN)** subtitles on YouTube and any video playing in Chrome.

---

## 🧩 New: VTT Chrome Extension (Free Install)

Minimal online subtitle overlay for **YouTube** and **any HTML5 video playing in Chrome**, built for **Persian (`فارسی`)** and **English (`EN`)**:

- **Works on YouTube & Any Online Video**: Automatically attaches to `<video>` elements in Chrome.
- **Persian (`FA`), English (`EN`), & Bilingual (`FA + EN`)**: Instant language switching from the popup or the subtle top-right video corner chip.
- **Calm, Sentence-Paced Reading**: Automatically merges rapid word-by-word auto-captions into full, readable 3.5s–5.5s sentence blocks.
- **Live Audio Speech Mode (`🎤`)**: Generates live online subtitles even for videos without uploaded caption tracks.
- **1-Click `.VTT` & `.SRT` Export**: Download captured subtitles anytime.

### ⬇ Free Installation

- **Option A — Full Chrome Extension (`vtt-chrome-extension.zip`)**:
  1. **[Download](https://github.com/momalekiii/VTT/raw/main/vtt-chrome-extension.zip)** and extract it to a folder.
  2. Open `chrome://extensions/` and turn **Developer mode** ON.
  3. Drag the extracted folder onto `chrome://extensions/` (or click **Load unpacked**).
- **Option B — 1-Click Userscript (`vtt-subtitles.user.js`)**:
  - If you have Tampermonkey or Violentmonkey installed, simply click **[Install](https://github.com/momalekiii/VTT/raw/main/vtt-subtitles.user.js)** for a 1-click install with no unzipping.

---

# Release notes (Awakens 🐉)

VTT is finally awake after a long sleep — and it finally makes actual `.vtt`
files. 😄

## ✨ Highlights

- 🧩 **Chrome Extension**: Minimal online Persian & English subtitle overlay for YouTube and any video in Chrome (`chrome-extension/`).
- 🧠 **New brain**: swapped the old online-only Google Web Speech API in the CLI for
  **Whisper** (via `faster-whisper`). Fully offline, ~100 languages, and much
  more accurate — especially for Persian/non-English audio.
- 🎬 **Real subtitles at last**: output is now genuine timestamped
  `.vtt` / `.srt`, not a single blob of plain text.
- 📁 **Batch mode**: point it at a folder, get subtitles for every video
  inside.
- ▶️ **YouTube/URL input**: `vtt_run "https://youtube.com/watch?v=..."` just
  works (needs the optional `[youtube]` extra).
- 🖥️ **GPU support**: `--device cuda` for faster runs.
- 🎚 **Model size control**: `--model tiny|base|small|medium|large-v3` to
  trade off speed vs. accuracy.

## ⚠️ Breaking change
Default CLI output is now `.vtt` instead of `.txt`. Pass `--format txt` if you
relied on the old plain-text output.

## 📦 Install CLI
```bash
pip install video-to-text-vtt
pip install "video-to-text-vtt[youtube]"   # optional, for URL input
```

## 🔧 CLI Example
```bash
vtt_run my_video.mp4 -lang fa --model medium
vtt_run ./my_videos --format all -o ./subtitles
```

## Migrating from v1

The CLI is backward-compatible for the common case (`python main.py path/to/video`),
but the default output is now a real `.vtt` file instead of a `.txt` file. Pass
`--format txt` if you want the old plain-text behavior.
