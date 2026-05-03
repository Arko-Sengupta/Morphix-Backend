import os
import logging
from Utils.GroqClient import GroqClient

logger = logging.getLogger(__name__)

class AudioToText:
    def __init__(self):
        try:
            self.client = GroqClient().client
            self.model = os.getenv("GROQ_MODEL_AUDIO_TO_TEXT")
            logger.info("AudioToText initialized with model: %s", self.model)
        except Exception:
            logger.error("Failed to initialize AudioToText", exc_info=True)
            raise

    def Convert(self, file_bytes: bytes = None, text_input: str = None, options: dict = None) -> dict:
        try:
            logger.info("Starting AudioToText conversion")
            ext = (options or {}).get("file_ext", "mp3")
            transcription = self.client.audio.transcriptions.create(
                model=self.model,
                file=(f"audio.{ext}", file_bytes),
            )
            logger.info("AudioToText conversion successful")
            return {
                "type": "text",
                "content": transcription.text,
                "filename": "transcript.txt",
                "mime_type": "text/plain",
            }
        except Exception:
            logger.error("AudioToText conversion failed", exc_info=True)
            raise