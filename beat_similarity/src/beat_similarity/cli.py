from __future__ import annotations

from pathlib import Path

import typer

from beat_similarity.pipeline import run
from beat_similarity.preprocess.separate import separate_drums_and_bass

app = typer.Typer(add_completion=False, help="Beat similarity analyzer (research CLI).")


@app.command()
def embed_drums(mp3_path: Path) -> None:
    """Run Demucs, embed drums stem with CLAP, print embedding shape."""

    run(mp3_path)


@app.command()
def separate(mp3_path: Path) -> None:
    """Run Demucs and print output stem paths."""

    stems = separate_drums_and_bass(mp3_path)
    print(f"stems dir: {stems.stems_dir}")
    print(f"drums: {stems.drums_wav}")
    print(f"bass:  {stems.bass_wav}")


if __name__ == "__main__":
    app()

