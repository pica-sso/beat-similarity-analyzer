"""Source separation orchestration helpers."""

from __future__ import annotations

from pathlib import Path

from .demucs import DemucsStems, run_demucs_separate


def separate_drums_and_bass(
    input_mp3: str | Path,
    *,
    work_dir: str | Path = ".beatsim_work",
    demucs_model: str = "htdemucs",
) -> DemucsStems:
    """Separate `input_mp3` into stems and return drums/bass paths."""

    work_dir = Path(work_dir)
    out_dir = work_dir / "demucs"
    return run_demucs_separate(input_audio=input_mp3, output_dir=out_dir, model=demucs_model)

