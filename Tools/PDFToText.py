import logging
from io import BytesIO
from pypdf import PdfReader

logger = logging.getLogger(__name__)

def ExtractPageText(page):
    try:
        return page.extract_text(extraction_mode="layout") or ""
    except TypeError:
        return page.extract_text() or ""

class PDFToText:
    def Convert(self, file_bytes: bytes = None, text_input: str = None, options: dict = None) -> dict:
        try:
            logger.info("Starting PDFToText conversion")
            pdf_reader = PdfReader(BytesIO(file_bytes))
            pages = [ExtractPageText(page) for page in pdf_reader.pages]
            text = "\n\n".join(pages).strip()
            logger.info("PDFToText conversion successful — %d pages", len(pages))
            return {
                "type": "text",
                "content": text,
                "filename": "extracted.txt",
                "mime_type": "text/plain",
            }
        except Exception:
            logger.error("PDFToText conversion failed", exc_info=True)
            raise