import os
import logging
from Tools.HFClient import HFClient

logger = logging.getLogger(__name__)

class ImageToText:
    def __init__(self):
        try:
            self.client = HFClient()
            self.model_id = os.getenv("HF_MODEL_IMAGE_TO_TEXT")
            logger.info("ImageToText initialized with model: %s", self.model_id)
        except Exception:
            logger.error("Failed to initialize ImageToText", exc_info=True)
            raise

    def Convert(self, file_bytes: bytes = None, text_input: str = None, options: dict = None) -> dict:
        try:
            logger.info("Starting ImageToText conversion")
            response = self.client.Call(self.model_id, binary_payload=file_bytes, content_type="image/jpeg")
            data = response.json()
            text = data[0].get("generated_text", "") if isinstance(data, list) else data.get("generated_text", "")
            logger.info("ImageToText conversion successful")
            return {
                "type": "text",
                "content": text,
                "filename": "extracted_text.txt",
                "mime_type": "text/plain",
            }
        except Exception:
            logger.error("ImageToText conversion failed", exc_info=True)
            raise