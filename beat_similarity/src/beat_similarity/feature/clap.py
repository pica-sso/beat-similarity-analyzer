"""CLAP embedding extraction (audio -> vector).

Uses Hugging Face `transformers` CLAP model.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import librosa
import soundfile as sf
import torch
from transformers import ClapModel, ClapProcessor


DEFAULT_CLAP_MODEL_ID = "laion/clap-htsat-unfused"


@dataclass(frozen=True)
class ClapBundle:
    model: ClapModel
    processor: ClapProcessor
    device: torch.device


def load_clap(
    *,
    model_id: str = DEFAULT_CLAP_MODEL_ID,
    device: str | None = None,
) -> ClapBundle:
    """Load CLAP model + processor."""

    if device is None:
        device = "cuda" if torch.cuda.is_available() else "cpu"
    torch_device = torch.device(device)

    processor = ClapProcessor.from_pretrained(model_id)
    model = ClapModel.from_pretrained(model_id)
    model.eval()
    model.to(torch_device)
    return ClapBundle(model=model, processor=processor, device=torch_device)


def clap_audio_embedding(
    bundle: ClapBundle,
    *,
    wav_path: str | Path,
) -> torch.Tensor:
    """Extract a single embedding vector from a .wav file.

    Returns a tensor shaped (1, D).
    """

    wav_path = Path(wav_path).expanduser().resolve()
    audio, sr = sf.read(str(wav_path), always_2d=False)

    # Convert to mono if needed.
    if getattr(audio, "ndim", 1) == 2:
        audio = audio.mean(axis=1)

    # CLAP feature extractor expects 48kHz audio.
    target_sr = 48_000
    if sr != target_sr:
        audio = librosa.resample(audio.astype("float32"), orig_sr=sr, target_sr=target_sr)
        sr = target_sr

    inputs = bundle.processor(audios=audio, sampling_rate=sr, return_tensors="pt")
    inputs = {k: v.to(bundle.device) for k, v in inputs.items()}

    with torch.no_grad():
        feats = bundle.model.get_audio_features(**inputs)
        # Normalize so cosine similarity behaves nicely later.
        feats = torch.nn.functional.normalize(feats, dim=-1)
        return feats

