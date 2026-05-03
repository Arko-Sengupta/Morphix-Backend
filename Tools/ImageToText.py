import os
import base64
import logging
from PIL import Image
from io import BytesIO
from Utils.GroqClient import GroqClient

logger = logging.getLogger(__name__)

class ImageToText:
    def __init__(self):
        try:
            self.client = GroqClient().client
            self.model = os.getenv("GROQ_MODEL_IMAGE_CAPTION")
            logger.info("ImageToText initialized with model: %s", self.model)
        except Exception:
            logger.error("Failed to initialize ImageToText", exc_info=True)
            raise

    def Convert(self, file_bytes: bytes = None, text_input: str = None, options: dict = None) -> dict:
        try:
            logger.info("Starting ImageToText conversion")
            image = Image.open(BytesIO(file_bytes)).convert("RGB")
            buffer = BytesIO()
            image.save(buffer, format="JPEG")
            image_b64 = base64.b64encode(buffer.getvalue()).decode()
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{
                    "role": "user",
                    "content": [
                        {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{image_b64}"}},
                        {"type": "text", "text": "Extract and return all text visible in this image exactly as it appears. Output only the extracted text, nothing else."}
                    ]
                }],
                max_tokens=2048
            )
            text = response.choices[0].message.content
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