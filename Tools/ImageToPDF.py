import base64
import logging
from io import BytesIO
from Tools.HFClient import HFClient
from reportlab.lib.enums import TA_JUSTIFY
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer
import os

logger = logging.getLogger(__name__)

class ImageToPDF:
    def __init__(self):
        try:
            self.client = HFClient()
            self.model_id = os.getenv("HF_MODEL_IMAGE_TO_TEXT")
            logger.info("ImageToPDF initialized with model: %s", self.model_id)
        except Exception:
            logger.error("Failed to initialize ImageToPDF", exc_info=True)
            raise

    def Convert(self, file_bytes: bytes = None, text_input: str = None, options: dict = None) -> dict:
        try:
            logger.info("Starting ImageToPDF conversion")
            response = self.client.Call(self.model_id, binary_payload=file_bytes, content_type="image/jpeg")
            data = response.json()
            text = data[0].get("generated_text", "") if isinstance(data, list) else data.get("generated_text", "")

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
