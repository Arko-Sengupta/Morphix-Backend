import os
import base64
import logging
from Utils.GroqClient import GroqClient

logger = logging.getLogger(__name__)

class ImageToCaption:
    def __init__(self):
        try:
            self.client = GroqClient().client
            self.model = os.getenv("GROQ_MODEL_IMAGE_CAPTION")
            logger.info("ImageToCaption initialized with model: %s", self.model)
        except Exception:
            logger.error("Failed to initialize ImageToCaption", exc_info=True)
            raise

    def Convert(self, file_bytes: bytes = None, text_input: str = None, options: dict = None) -> dict:
        try:
            logger.info("Starting ImageToCaption conversion")
            image_b64 = base64.b64encode(file_bytes).decode()
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{
                    "role": "user",
                    "content": [
                        {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{image_b64}"}},
                        {"type": "text", "text": "Describe this image in one or two concise sentences."}
                    ]
                }],
                max_tokens=200
            )
            caption = response.choices[0].message.content
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