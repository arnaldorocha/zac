"""
Speech-to-Text module using faster-whisper and sounddevice.
"""

import logging
import tempfile
from pathlib import Path
from typing import Optional

import numpy as np
import sounddevice as sd
from scipy.io.wavfile import write as write_wav

logger = logging.getLogger(__name__)


class SpeechToText:
    """Handles speech-to-text conversion using faster-whisper."""

    def __init__(
        self,
        model_name: str = "base",
        sample_rate: int = 16000,
        silence_threshold: float = 500.0,
        silence_duration: float = 1.5,
    ):
        self.model_name = model_name
        self.sample_rate = sample_rate
        self.silence_threshold = silence_threshold
        self.silence_duration = silence_duration
        self._model = self._load_model()

    def _load_model(self):
        try:
            from faster_whisper import WhisperModel
        except ImportError:
            logger.error("faster-whisper not installed. Install with: pip install faster-whisper")
            return None

        try:
            logger.info(f"Loading Whisper model: {self.model_name}")
            model = WhisperModel(self.model_name, device="cpu", compute_type="int8")
            logger.info("Whisper model loaded successfully")
            return model
        except Exception as exc:
            logger.error(f"Failed to load Whisper model: {exc}")
            return None

    def _compute_rms(self, frames: np.ndarray) -> float:
        if frames.size == 0:
            return 0.0
        return float(np.sqrt(np.mean(np.square(frames.astype(np.float32)))))

    def _is_silent(self, frames: np.ndarray) -> bool:
        return self._compute_rms(frames) < self.silence_threshold

    def _record_audio(self, timeout: int) -> Optional[Path]:
        chunk_seconds = 0.25
        max_chunks = int(timeout / chunk_seconds)
        silence_chunks_required = int(self.silence_duration / chunk_seconds)
        silence_counter = 0
        recorded_frames = []

        try:
            with sd.InputStream(
                samplerate=self.sample_rate,
                channels=1,
                dtype="int16",
                blocksize=int(self.sample_rate * chunk_seconds),
            ) as stream:
                logger.info("Recording audio from microphone")

                for chunk_index in range(max_chunks):
                    frames, _ = stream.read(int(self.sample_rate * chunk_seconds))
                    chunk = np.squeeze(frames)
                    recorded_frames.append(chunk)

                    if self._is_silent(chunk):
                        silence_counter += 1
                        if silence_counter >= silence_chunks_required and chunk_index > 0:
                            logger.info("Silence detected, stopping recording")
                            break
                    else:
                        silence_counter = 0

                if not recorded_frames:
                    logger.warning("No audio captured")
                    return None

                audio_data = np.concatenate(recorded_frames)
                temp_wav = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
                temp_path = Path(temp_wav.name)
                temp_wav.close()
                write_wav(str(temp_path), self.sample_rate, audio_data)
                return temp_path

        except Exception as exc:
            logger.error(f"Audio recording failed: {exc}")
            return None

    def listen(self, timeout: int = 15) -> Optional[str]:
        """Listen for speech and return transcribed text."""
        if not self._model:
            logger.error("Speech recognition model is not initialized")
            return None

        audio_path = self._record_audio(timeout)
        if not audio_path:
            return None

        try:
            logger.info(f"Transcribing audio: {audio_path}")
            result = self._model.transcribe(
                str(audio_path),
                beam_size=5,
                language=None,
                vad_filter=False,
            )

            transcript = []
            for segment in result:
                if hasattr(segment, "text"):
                    transcript.append(segment.text)
                elif isinstance(segment, dict) and "text" in segment:
                    transcript.append(segment["text"])

            text = " ".join(transcript).strip()
            if text:
                logger.info(f"Transcribed text: {text}")
            else:
                logger.warning("Transcription returned no text")
            return text or None
        except Exception as exc:
            logger.error(f"Transcription failed: {exc}")
            return None
        finally:
            try:
                if audio_path.exists():
                    audio_path.unlink()
            except Exception:
                pass