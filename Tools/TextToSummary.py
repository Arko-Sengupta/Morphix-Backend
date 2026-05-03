import os
import logging
from Utils.GroqClient import GroqClient

logger = logging.getLogger(__name__)

class TextToSummary:
    def __init__(self):
        try:
            self.client = GroqClient().client
            self.model = os.getenv("GROQ_MODEL_TEXT_SUMMARY")
            logger.info("TextToSummary initialized with model: %s", self.model)
        except Exception:
            logger.error("Failed to initialize TextToSummary", exc_info=True)
            raise

    def Convert(self, file_bytes: bytes = None, text_input: str = None, options: dict = None) -> dict:
        try:
            logger.info("Starting TextToSummary conversion")
            text = text_input or (file_bytes.decode("utf-8", errors="replace") if file_bytes else "")
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "Summarize the following text concisely, preserving key points."},
                    {"role": "user", "content": text}
                ],
                max_tokens=512
            )
            summary = response.choices[0].message.content
            logger.info("TextToSummary conversion successful")
            return {
                "type": "text",
                "content": summary,
                "filename": "summary.txt",
                "mime_type": "text/plain",
            }
        except Exception:
            logger.error("TextToSummary conversion failed", exc_info=True)
            raise