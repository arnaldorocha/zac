"""
Text-to-Speech module using Microsoft Edge TTS.
"""
import asyncio
import logging
import tempfile
import threading
import time
from pathlib import Path
from typing import Optional

logger = logging.getLogger(__name__)


class TextToSpeech:
    """Handles text-to-speech using edge-tts."""

    def __init__(
        self,
        voice_name: str = "pt-BR-AntonioNeural",
        volume: float = 1.0,
    ):
        self.voice_name = voice_name
        self.volume = max(0.0, min(volume, 1.0))
        self._stop_event = threading.Event()
        self._playback_thread: Optional[threading.Thread] = None
        self._initialize_audio()

    def _initialize_audio(self) -> None:
        try:
            import pygame  # noqa: F401

            pygame.mixer.init()
            pygame.mixer.music.set_volume(self.volume)
            logger.info("TextToSpeech audio backend initialized")
        except ImportError:
            logger.error("pygame not installed. Install with: pip install pygame")
        except Exception as exc:
            logger.error(f"Failed to initialize audio backend: {exc}")

    def _get_temp_audio_file(self) -> Path:
        temp_file = tempfile.NamedTemporaryFile(suffix=".mp3", delete=False)
        path = Path(temp_file.name)
        temp_file.close()
        return path

    async def _generate_audio(self, text: str, output_path: str) -> None:
        try:
            from edge_tts import Communicate
        except ImportError:
            logger.error("edge-tts not installed. Install with: pip install edge-tts")
            raise

        communicate = Communicate(text, voice=self.voice_name)
        await communicate.save(output_path)

    def _render_text_to_file(self, text: str, output_path: Path) -> None:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            loop.run_until_complete(self._generate_audio(text, str(output_path)))
        finally:
            loop.close()

    def _play_audio(self, audio_path: Path, block: bool = True) -> bool:
        try:
            import pygame
        except ImportError:
            logger.error("pygame is required to play audio. Install with: pip install pygame")
            return False

        try:
            pygame.mixer.music.load(str(audio_path))
            pygame.mixer.music.set_volume(self.volume)
            pygame.mixer.music.play()

            if not block:
                return True

            while pygame.mixer.music.get_busy():
                if self._stop_event.is_set():
                    pygame.mixer.music.stop()
                    logger.info("Speech playback interrupted")
                    break
                time.sleep(0.1)

            return True
        except Exception as exc:
            logger.error(f"Error during audio playback: {exc}")
            return False

    def speak(self, text: str) -> bool:
        """Speak the given text synchronously."""
        if not text:
            logger.warning("No text provided to speak")
            return False

        audio_path = self._get_temp_audio_file()
        try:
            self._render_text_to_file(text, audio_path)
            self._stop_event.clear()
            return self._play_audio(audio_path, block=True)
        except Exception as exc:
            logger.error(f"Failed to speak text: {exc}")
            return False
        finally:
            try:
                if audio_path.exists():
                    audio_path.unlink()
            except Exception:
                pass

    def _async_speak_worker(self, text: str) -> None:
        audio_path = self._get_temp_audio_file()
        try:
            self._render_text_to_file(text, audio_path)
            self._stop_event.clear()
            self._play_audio(audio_path, block=True)
        except Exception as exc:
            logger.error(f"Async speech failed: {exc}")
        finally:
            try:
                if audio_path.exists():
                    audio_path.unlink()
            except Exception:
                pass

    def speak_async(self, text: str) -> bool:
        """Speak the given text asynchronously."""
        if not text:
            logger.warning("No text provided to speak asynchronously")
            return False

        if self._playback_thread and self._playback_thread.is_alive():
            self.stop()
            self._playback_thread.join(timeout=1)

        self._playback_thread = threading.Thread(
            target=self._async_speak_worker,
            args=(text,),
            daemon=True,
        )
        self._playback_thread.start()
        return True

    def stop(self) -> None:
        """Stop current speech playback."""
        self._stop_event.set()
        try:
            import pygame
            pygame.mixer.music.stop()
        except ImportError:
            pass
        except Exception as exc:
            logger.error(f"Failed to stop speech playback: {exc}")

    def set_voice(self, voice_name: str) -> None:
        """Set the voice name used by edge-tts."""
        self.voice_name = voice_name
        logger.info(f"TTS voice set to {voice_name}")
