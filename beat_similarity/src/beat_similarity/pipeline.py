"""
Pipeline orchestrator.

Keep this thin: call into ingestion/preprocess/feature/storage/search/report modules.
"""

from __future__ import annotations

from pathlib import Path

from beat_similarity.feature.clap import clap_audio_embedding, load_clap
from beat_similarity.preprocess.separate import separate_drums_and_bass


def run(mp3_path: str | Path) -> None:
    """Minimal pipeline: mp3 -> demucs -> CLAP embedding for drums -> print shape."""

    stems = separate_drums_and_bass(mp3_path)
    bundle = load_clap()
    emb = clap_audio_embedding(bundle, wav_path=stems.drums_wav)
    print(f"drums embedding shape: {tuple(emb.shape)}")

