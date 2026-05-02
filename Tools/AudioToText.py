import os
import logging
from Tools.HFClient import HFClient

logger = logging.getLogger(__name__)

class AudioToText:
    def __init__(self):
        try:
            self.client = HFClient()
            self.model_id = os.getenv("HF_MODEL_AUDIO_TO_TEXT")
            logger.info("AudioToText initialized with model: %s", self.model_id)
        except Exception:
            logger.error("Failed to initialize AudioToText", exc_info=True)
            raise

    def Convert(self, file_bytes: bytes = None, text_input: str = None, options: dict = None) -> dict:
        try:
            logger.info("Starting AudioToText conversion")
            response = self.client.Call(self.model_id, binary_payload=file_bytes, content_type="audio/mpeg")
            data = response.json()
            text = data.get("text", "")
            logger.info("AudioToText conversion successful")
            return {
                "type": "text",
                "content": text,
                "filename": "transcript.txt",
                "mime_type": "text/plain",
            }
        except Exception:
            logger.error("AudioToText conversion failed", exc_info=True)
            raise