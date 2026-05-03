import logging
import numpy as np
from PIL import Image
from io import BytesIO
from rapidocr_onnxruntime import RapidOCR

logger = logging.getLogger(__name__)
_engine = None

def GetEngine():
    global _engine
    if _engine is None:
        _engine = RapidOCR()
    return _engine

class ImageToText:
    def Convert(self, file_bytes: bytes = None, text_input: str = None, options: dict = None) -> dict:
        try:
            logger.info("Starting ImageToText conversion")
            image = np.array(Image.open(BytesIO(file_bytes)).convert("RGB"))
            result, _ = GetEngine()(image)
            text = "\n".join([item[1] for item in result]) if result else ""
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