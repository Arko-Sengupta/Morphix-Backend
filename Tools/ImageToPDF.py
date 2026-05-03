import os
import base64
import logging
from io import BytesIO
from PIL import Image
from Utils.GroqClient import GroqClient
from reportlab.lib.enums import TA_JUSTIFY
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer

logger = logging.getLogger(__name__)

class ImageToPDF:
    def __init__(self):
        try:
            self.client = GroqClient().client
            self.model = os.getenv("GROQ_MODEL_IMAGE_CAPTION")
            logger.info("ImageToPDF initialized with model: %s", self.model)
        except Exception:
            logger.error("Failed to initialize ImageToPDF", exc_info=True)
            raise

    def Convert(self, file_bytes: bytes = None, text_input: str = None, options: dict = None) -> dict:
        try:
            logger.info("Starting ImageToPDF conversion")
            image = Image.open(BytesIO(file_bytes)).convert("RGB")
            buffer = BytesIO()
            image.save(buffer, format="JPEG")
            image_b64 = base64.b64encode(buffer.getvalue()).decode()
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{
                    "role": "user",
                    "content": [
                        {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{image_b64}"}},
                        {"type": "text", "text": "Extract and return all text visible in this image exactly as it appears. Output only the extracted text, nothing else."}
                    ]
                }],
                max_tokens=2048
            )
            text = response.choices[0].message.content

            pdf_buffer = BytesIO()
            doc = SimpleDocTemplate(pdf_buffer, pagesize=letter, title="Document")
            styles = getSampleStyleSheet()
            styles.add(ParagraphStyle(name="Justified", alignment=TA_JUSTIFY, fontName="Times-Roman", fontSize=12, leading=24))
            flowables = []
            for line in text.split("\n"):
                if line.strip():
                    flowables.append(Paragraph(line, styles["Justified"]))
                    flowables.append(Spacer(1, 6))
            doc.build(flowables)
            pdf_buffer.seek(0)
            logger.info("ImageToPDF conversion successful")
            return {
                "type": "binary",
                "content": base64.b64encode(pdf_buffer.getvalue()).decode(),
                "filename": "document.pdf",
                "mime_type": "application/pdf",
            }
        except Exception:
            logger.error("ImageToPDF conversion failed", exc_info=True)
            raise