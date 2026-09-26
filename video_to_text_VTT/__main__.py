from __future__ import annotations

import sys
from pathlib import Path
from typing import Optional, Tuple

import click

from . import audio_extractor, transcriber, youtube
from .subtitle_writer import WRITERS

VIDEO_EXTENSIONS = {".mp4", ".mkv", ".mov", ".avi", ".webm", ".flv"}


def _iter_inputs(path_or_url: str) -> Tuple[list, bool]:
    """Return (list_of_paths_or_urls, is_batch)."""
    if youtube.looks_like_url(path_or_url):
        return [path_or_url], False

    p = Path(path_or_url)
    if p.is_dir():
        files = sorted(
            f for f in p.iterdir()
            if f.suffix.lower() in VIDEO_EXTENSIONS | audio_extractor.AUDIO_EXTENSIONS
        )
        return files, True
    return [p], False


def _resolve_source(item, offset: Optional[float], duration: Optional[float]) -> Path:
    if isinstance(item, str) and youtube.looks_like_url(item):
        click.echo(f"Downloading: {item}")
        downloaded = youtube.download_audio(item)
        if offset or duration:
            return audio_extractor.extract_audio(downloaded, offset=offset, duration=duration)
        return downloaded
    return audio_extractor.extract_audio(item, offset=offset, duration=duration)


def _output_path_for(source_name: str, output: Optional[str], fmt: str, is_batch: bool) -> Path:
    if output and not is_batch:
        return Path(output)
    stem = Path(source_name).stem
    if output and is_batch:
        return Path(output) / f"{stem}.{fmt}"
    return Path(f"{stem}.{fmt}")


@click.command()
@click.argument("path", type=str)
@click.option("--duration", type=float, default=None, help="Audio length to transcribe, in seconds.")
@click.option("--offset", type=float, default=None, help="How far from the start to begin, in seconds.")
@click.option("-lang", "--language", "language", type=str, default=None,
              help="Language code (e.g. en, fa, es). Omit to auto-detect.")
@click.option("--model", "model_size", type=click.Choice(
    ["tiny", "base", "small", "medium", "large-v3"]), default="small",
    help="Whisper model size. Bigger = more accurate, slower.")
@click.option("--device", type=click.Choice(["auto", "cpu", "cuda"]), default="auto",
              help="Run the model on CPU or GPU.")
@click.option("-o", "--output", "output", type=str, default=None,
              help="Output file (single input) or output directory (batch/folder input).")
@click.option("--format", "fmt", type=click.Choice(["vtt", "srt", "txt", "all"]), default="vtt",
              help="Subtitle/output format. 'all' writes vtt+srt+txt.")
def main(path, duration, offset, language, model_size, device, output, fmt):
    """Extract speech from PATH (a video/audio file, a folder of them, or a
    YouTube/URL) and write real timestamped subtitles (.vtt / .srt) or plain text.
    """
    items, is_batch = _iter_inputs(path)
    if not items:
        click.echo("No supported video/audio files found.", err=True)
        sys.exit(1)

    if is_batch and output:
        Path(output).mkdir(parents=True, exist_ok=True)

    formats = ["vtt", "srt", "txt"] if fmt == "all" else [fmt]

    for item in items:
        label = str(item)
        click.echo(f"Transcribing: {label}")
        audio_path = _resolve_source(item, offset, duration)
        segments = transcriber.transcribe(
            audio_path, model_size=model_size, language=language, device=device,
        )
        if not segments:
            click.echo(f"  (no speech detected in {label})")
            continue
        for f in formats:
            out_path = _output_path_for(label, output, f, is_batch)
            WRITERS[f](segments, out_path)
            click.echo(f"  -> {out_path}")


if __name__ == "__main__":
    main()
