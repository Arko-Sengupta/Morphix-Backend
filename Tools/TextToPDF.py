import base64
import logging
from io import BytesIO
from reportlab.lib.enums import TA_JUSTIFY
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer

logger = logging.getLogger(__name__)

class TextToPDF:
    def Convert(self, file_bytes: bytes = None, text_input: str = None, options: dict = None) -> dict:
        try:
            logger.info("Starting TextToPDF conversion")
            text = text_input or (file_bytes.decode("utf-8", errors="replace") if file_bytes else "")

            buffer = BytesIO()
            doc = SimpleDocTemplate(buffer, pagesize=letter, title="Document")
            styles = getSampleStyleSheet()
            styles.add(ParagraphStyle(name="Justified", alignment=TA_JUSTIFY, fontName="Times-Roman", fontSize=12, leading=24))

            flowables = []
            for para in text.split("\n\n"):
                if para.strip():
                    flowables.append(Paragraph(para.replace("\n", "<br/>"), styles["Justified"]))
                    flowables.append(Spacer(1, 12))

            doc.build(flowables)
            buffer.seek(0)
            logger.info("TextToPDF conversion successful")
            return {
                "type": "binary",
                "content": base64.b64encode(buffer.getvalue()).decode(),
                "filename": "document.pdf",
                "mime_type": "application/pdf",
            }
        except Exception:
            logger.error("TextToPDF conversion failed", exc_info=True)
            raise