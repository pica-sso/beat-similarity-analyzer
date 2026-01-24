"""Demucs-based source separation (drums/bass/etc.).

This module intentionally uses the Demucs CLI via subprocess to avoid tightly
coupling to Demucs' internal Python APIs (which change across versions).
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import subprocess
import sys


@dataclass(frozen=True)
class DemucsStems:
    """Paths to the stems we care about for similarity."""

    drums_wav: Path
    bass_wav: Path
    stems_dir: Path  # directory that contains all stems (drums/bass/other/vocals...)


def run_demucs_separate(
    *,
    input_audio: str | Path,
    output_dir: str | Path,
    model: str = "htdemucs",
) -> DemucsStems:
    """Run Demucs on an audio file and return paths to drums/bass stems.

    Demucs typically writes stems to:
      <output_dir>/separated/<model>/<track_name>/{drums,bass,other,vocals}.wav

    We *don't* assume the exact structure is stable; we search under output_dir
    for `drums.wav` and `bass.wav` that share a parent folder.
    """

    input_audio = Path(input_audio).expanduser().resolve()
    output_dir = Path(output_dir).expanduser().resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    if not input_audio.exists():
        raise FileNotFoundError(f"Input audio not found: {input_audio}")

    # Demucs CLI: `python -m demucs -n htdemucs -o <out> <file>`
    # IMPORTANT: use the *current* interpreter (venv) so `demucs` is found.
    cmd = [sys.executable, "-m", "demucs", "-n", model, "-o", str(output_dir), str(input_audio)]
    try:
        subprocess.run(cmd, check=True, capture_output=True, text=True)
    except subprocess.CalledProcessError as e:
        # Surface demucs stderr/stdout to make install/ffmpeg issues obvious.
        msg = [
            "Demucs failed.",
            f"Command: {e.cmd}",
        ]
        if e.stdout:
            msg.append("--- demucs stdout ---")
            msg.append(e.stdout)
        if e.stderr:
            msg.append("--- demucs stderr ---")
            msg.append(e.stderr)
        raise RuntimeError("\n".join(msg)) from e

    drums = list(output_dir.rglob("drums.wav"))
    bass = list(output_dir.rglob("bass.wav"))
    if not drums or not bass:
        raise RuntimeError(
            "Demucs finished but could not find expected stems under output_dir. "
            f"Found drums={len(drums)}, bass={len(bass)} in {output_dir}"
        )

    # Pick a pair that lives in the same parent directory.
    bass_by_parent = {p.parent.resolve(): p.resolve() for p in bass}
    for d in drums:
        parent = d.parent.resolve()
        if parent in bass_by_parent:
            return DemucsStems(drums_wav=d.resolve(), bass_wav=bass_by_parent[parent], stems_dir=parent)

    raise RuntimeError(
        "Demucs produced stems, but no drums/bass pair shared the same output folder. "
        f"Example drums={drums[0]} bass={bass[0]}"
    )

