import base64
import logging
import numpy as np
from PIL import Image
from io import BytesIO
from rapidocr_onnxruntime import RapidOCR
from reportlab.lib.enums import TA_JUSTIFY
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer

logger = logging.getLogger(__name__)
_engine = None

def GetEngine():
    global _engine
    if _engine is None:
        _engine = RapidOCR()
    return _engine

class ImageToPDF:
    def Convert(self, file_bytes: bytes = None, text_input: str = None, options: dict = None) -> dict:
        try:
            logger.info("Starting ImageToPDF conversion")
            image = np.array(Image.open(BytesIO(file_bytes)).convert("RGB"))
            result, _ = GetEngine()(image)
            text = "\n".join([item[1] for item in result]) if result else ""

            buffer = BytesIO()
            doc = SimpleDocTemplate(buffer, pagesize=letter, title="Document")
            styles = getSampleStyleSheet()
            styles.add(ParagraphStyle(name="Justified", alignment=TA_JUSTIFY, fontName="Times-Roman", fontSize=12, leading=24))

            flowables = []
            for line in text.split("\n"):
                if line.strip():
                    flowables.append(Paragraph(line, styles["Justified"]))
                    flowables.append(Spacer(1, 6))

            doc.build(flowables)
            buffer.seek(0)
            logger.info("ImageToPDF conversion successful")
            return {
                "type": "binary",
                "content": base64.b64encode(buffer.getvalue()).decode(),
                "filename": "document.pdf",
                "mime_type": "application/pdf",
            }
        except Exception:
            logger.error("ImageToPDF conversion failed", exc_info=True)
            raise
