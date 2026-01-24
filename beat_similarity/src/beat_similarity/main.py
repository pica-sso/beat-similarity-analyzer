"""
Package entrypoint for running from source.

This exists so you can run:
  python .\\src\\beat_similarity\\main.py <command> ...

on Windows without installing the package.
"""

from __future__ import annotations

import sys
from pathlib import Path


def _ensure_src_on_path() -> None:
    # When executing this file directly, Python puts `.../src/beat_similarity` on sys.path,
    # which makes `import beat_similarity` fail (it needs `.../src`).
    src_dir = Path(__file__).resolve().parents[1]
    if str(src_dir) not in sys.path:
        sys.path.insert(0, str(src_dir))


def main() -> None:
    _ensure_src_on_path()
    from beat_similarity.cli import app  # local import after sys.path fix

    app()


if __name__ == "__main__":
    main()

