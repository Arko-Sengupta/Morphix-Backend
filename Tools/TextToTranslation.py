import os
import logging
from Utils.GroqClient import GroqClient

logger = logging.getLogger(__name__)

class TextToTranslation:
    def __init__(self):
        try:
            self.client = GroqClient().client
            self.model = os.getenv("GROQ_MODEL_TEXT_TRANSLATION")
            logger.info("TextToTranslation initialized with model: %s", self.model)
        except Exception:
            logger.error("Failed to initialize TextToTranslation", exc_info=True)
            raise

    def Convert(self, file_bytes: bytes = None, text_input: str = None, options: dict = None) -> dict:
        try:
            logger.info("Starting TextToTranslation conversion")
            text = text_input or (file_bytes.decode("utf-8", errors="replace") if file_bytes else "")
            target = (options or {}).get("target_language", "French")
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": f"Translate the following text to {target}. Output only the translation, nothing else."},
                    {"role": "user", "content": text}
                ],
                max_tokens=2048
            )
            translation = response.choices[0].message.content
            logger.info("TextToTranslation conversion successful: %s", target)
            return {
                "type": "text",
                "content": translation,
                "filename": f"translation_{target.lower()}.txt",
                "mime_type": "text/plain",
            }
        except Exception:
            logger.error("TextToTranslation conversion failed", exc_info=True)
            raise