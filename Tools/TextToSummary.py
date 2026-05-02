import os
import logging
from Tools.HFClient import HFClient

logger = logging.getLogger(__name__)
CHUNK_CHARS = 3000

def ChunkText(text):
    if len(text) <= CHUNK_CHARS:
        return [text]
    paragraphs = text.split("\n\n")
    chunks, current = [], ""
    for para in paragraphs:
        if len(current) + len(para) + 2 <= CHUNK_CHARS:
            current = (current + "\n\n" + para).strip()
        else:
            if current:
                chunks.append(current)
            current = para[:CHUNK_CHARS]
    if current:
        chunks.append(current)
    return chunks or [text[:CHUNK_CHARS]]

class TextToSummary:
    def __init__(self):
        try:
            self.client = HFClient()
            self.model_id = os.getenv("HF_MODEL_TEXT_SUMMARY")
            logger.info("TextToSummary initialized with model: %s", self.model_id)
        except Exception:
            logger.error("Failed to initialize TextToSummary", exc_info=True)
            raise

    def Convert(self, file_bytes: bytes = None, text_input: str = None, options: dict = None) -> dict:
        try:
            logger.info("Starting TextToSummary conversion")
            text = text_input or (file_bytes.decode("utf-8", errors="replace") if file_bytes else "")
            chunks = ChunkText(text)
            logger.info("TextToSummary processing %d chunk(s)", len(chunks))
            summaries = []
            for chunk in chunks:
                response = self.client.Call(
                    self.model_id,
                    json_payload={"inputs": chunk, "parameters": {"max_length": 512, "min_length": 30}}
                )
                data = response.json()
                summaries.append(data[0]["summary_text"] if isinstance(data, list) else data.get("summary_text", ""))
            summary = " ".join(summaries)
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