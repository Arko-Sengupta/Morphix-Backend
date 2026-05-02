import os
import logging
from Tools.HFClient import HFClient

logger = logging.getLogger(__name__)

class ImageToCaption:
    def __init__(self):
        try:
            self.client = HFClient()
            self.model_id = os.getenv("HF_MODEL_IMAGE_CAPTION")
            logger.info("ImageToCaption initialized with model: %s", self.model_id)
        except Exception:
            logger.error("Failed to initialize ImageToCaption", exc_info=True)
            raise

    def Convert(self, file_bytes: bytes = None, text_input: str = None, options: dict = None) -> dict:
        try:
            logger.info("Starting ImageToCaption conversion")
            response = self.client.Call(self.model_id, binary_payload=file_bytes, content_type="image/jpeg")
            data = response.json()
            caption = data[0].get("generated_text", "") if isinstance(data, list) else data.get("generated_text", "")
            logger.info("ImageToCaption conversion successful")
            return {
                "type": "text",
                "content": caption,
                "filename": "caption.txt",
                "mime_type": "text/plain",
            }
        except Exception:
            logger.error("ImageToCaption conversion failed", exc_info=True)
            raise
