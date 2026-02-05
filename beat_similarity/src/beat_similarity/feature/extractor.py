"""
Module for feature extraction using AI models.
Uses an injected logger to report internal model processing steps.
"""

import librosa
import torch
from transformers import AutoProcessor, ClapModel

class BeatFeatureExtractor:
    def __init__(self, logger):
        # Use the injected logger
        self.logger = logger
        self.model_name = "laion/clap-htsat-unfused"

        self.logger.info(f"[FeatureExtractor] Initializing CLAP model: {self.model_name}")
        try:
            self.processor = AutoProcessor.from_pretrained(self.model_name)
            self.model = ClapModel.from_pretrained(self.model_name)
            self.device = "cuda" if torch.cuda.is_available() else "cpu"
            self.model.to(self.device)
            self.logger.info(f"[FeatureExtractor] Model successfully moved to device: {self.device}")
        except Exception as e:
            self.logger.error(f"[FeatureExtractor] Error loading AI model: {str(e)}")
            raise

    def extract_vector(self, file_path):
        """Extracts a feature vector from an audio file."""
        try:
            self.logger.info(f"[FeatureExtractor] Processing audio for vectorization: {file_path}")
            y, sr = librosa.load(file_path, sr=48000)
            y = y[:48000 * 10]  # First 10 seconds

            inputs = self.processor(audios=y, return_tensors="pt", sampling_rate=48000).to(self.device)
            with torch.no_grad():
                audio_embeds = self.model.get_audio_features(**inputs)

            vector = audio_embeds.cpu().numpy()
            self.logger.info(f"[FeatureExtractor] Vector extraction complete. Shape: {vector.shape}")
            return vector
        except Exception as e:
            self.logger.error(f"[FeatureExtractor] Failed to extract features: {str(e)}")
            raise