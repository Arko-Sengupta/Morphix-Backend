import base64
import logging
import easyocr
import numpy as np
from PIL import Image
from io import BytesIO
from reportlab.lib.enums import TA_JUSTIFY
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer

logger = logging.getLogger(__name__)
reader = None

def GetReader():
    try:
        global reader
        if reader is None:
            logger.info("Initializing EasyOCR reader")
            reader = easyocr.Reader(["en"])
        return reader
    except Exception:
        logger.error("Failed to initialize EasyOCR reader", exc_info=True)
        raise

def GroupLines(text_data, threshold=15):
    if not text_data:
        return ""
    sorted_data = sorted(text_data, key=lambda item: (item[0][0][1], item[0][0][0]))
    lines = []
    current_y = sorted_data[0][0][0][1]
    current_line = []
    for bbox, text, _ in sorted_data:
        y = bbox[0][1]
        if abs(y - current_y) <= threshold:
            current_line.append(text)
        else:
            lines.append(" ".join(current_line))
            current_line = [text]
            current_y = y
    if current_line:
        lines.append(" ".join(current_line))
    return "\n".join(lines)

class ImageToPDF:
    def Convert(self, file_bytes: bytes = None, text_input: str = None, options: dict = None) -> dict:
        try:
            logger.info("Starting ImageToPDF conversion")
            image = Image.open(BytesIO(file_bytes))
            text_data = GetReader().readtext(np.array(image))
            text = GroupLines(text_data)

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