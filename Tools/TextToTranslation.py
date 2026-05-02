import os
import re
import logging
from Tools.HFClient import HFClient

logger = logging.getLogger(__name__)
CHUNK_CHARS = 400

LANGUAGE_CODES = {
    "Arabic":     "ar",
    "Chinese":    "zh",
    "Dutch":      "nl",
    "French":     "fr",
    "German":     "de",
    "Italian":    "it",
    "Japanese":   "jap",
    "Portuguese": "pt",
    "Russian":    "ru",
    "Spanish":    "es",
}

def ChunkBySentences(text):
    sentences = re.split(r'(?<=[.!?])\s+', text.strip())
    chunks, current = [], ""
    for sentence in sentences:
        if len(current) + len(sentence) + 1 <= CHUNK_CHARS:
            current = (current + " " + sentence).strip()
        else:
            if current:
                chunks.append(current)
            current = sentence[:CHUNK_CHARS]
    if current:
        chunks.append(current)
    return chunks or [text[:CHUNK_CHARS]]

class TextToTranslation:
    def __init__(self):
        try:
            self.client = HFClient()
            self.model_prefix = os.getenv("HF_MODEL_TEXT_TRANSLATION")
            logger.info("TextToTranslation initialized with prefix: %s", self.model_prefix)
        except Exception:
            logger.error("Failed to initialize TextToTranslation", exc_info=True)
            raise

    def Convert(self, file_bytes: bytes = None, text_input: str = None, options: dict = None) -> dict:
        try:
            logger.info("Starting TextToTranslation conversion")
            text = text_input or (file_bytes.decode("utf-8", errors="replace") if file_bytes else "")
            target = (options or {}).get("target_language", "French")
            model_id = self.model_prefix + LANGUAGE_CODES.get(target, "fr")
            chunks = ChunkBySentences(text)
            logger.info("TextToTranslation processing %d chunk(s) to %s", len(chunks), target)
            translations = []
            for chunk in chunks:
                response = self.client.Call(model_id, json_payload={"inputs": chunk})
                data = response.json()
                translations.append(data[0]["translation_text"] if isinstance(data, list) else data.get("translation_text", ""))
            translation = " ".join(translations)
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