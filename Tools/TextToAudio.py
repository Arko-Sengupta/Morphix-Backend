import os
import base64
import logging
from Tools.HFClient import HFClient

logger = logging.getLogger(__name__)

class TextToAudio:
    def __init__(self):
        try:
            self.client = HFClient()
            self.model_id = os.getenv("HF_MODEL_TEXT_AUDIO")
            logger.info("TextToAudio initialized with model: %s", self.model_id)
        except Exception:
            logger.error("Failed to initialize TextToAudio", exc_info=True)
            raise

    def Convert(self, file_bytes: bytes = None, text_input: str = None, options: dict = None) -> dict:
        try:
            logger.info("Starting TextToAudio conversion")
            text = text_input or (file_bytes.decode("utf-8", errors="replace") if file_bytes else "")
            response = self.client.Call(self.model_id, json_payload={"inputs": text})
            audio_bytes = response.content
            logger.info("TextToAudio conversion successful")
            return {
                "type": "binary",
                "content": base64.b64encode(audio_bytes).decode(),
                "filename": "speech.flac",
                "mime_type": "audio/flac",
            }
        except Exception:
            logger.error("TextToAudio conversion failed", exc_info=True)
            raise