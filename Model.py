import logging
from dotenv import load_dotenv

from Tools.PDFToText import PDFToText
from Tools.TextToPDF import TextToPDF
from Tools.ImageToPDF import ImageToPDF
from Tools.AudioToText import AudioToText
from Tools.ImageToText import ImageToText
from Tools.TextToAudio import TextToAudio
from Tools.TextToSummary import TextToSummary
from Tools.ImageToCaption import ImageToCaption
from Tools.TextToTranslation import TextToTranslation

load_dotenv(".env")
logger = logging.getLogger(__name__)

CONVERSIONS = [
    {
        "id": "image_to_text",
        "label": "Image → Text",
        "description": "Extract text from an image using OCR",
        "icon": "ScanText",
        "input_mode": "file",
        "file_types": ["jpg", "jpeg", "png", "bmp", "tiff"],
        "options": [],
    },
    {
        "id": "image_to_pdf",
        "label": "Image → PDF",
        "description": "Convert an image to a searchable PDF via OCR",
        "icon": "FileImage",
        "input_mode": "file",
        "file_types": ["jpg", "jpeg", "png", "bmp", "tiff"],
        "options": [],
    },
    {
        "id": "image_to_caption",
        "label": "Image → Caption",
        "description": "Generate an AI caption describing the image",
        "icon": "MessageSquareText",
        "input_mode": "file",
        "file_types": ["jpg", "jpeg", "png"],
        "options": [],
    },
    {
        "id": "audio_to_text",
        "label": "Audio → Text",
        "description": "Transcribe spoken audio to text using Whisper",
        "icon": "Mic",
        "input_mode": "file",
        "file_types": ["mp3", "wav", "flac", "ogg", "m4a"],
        "options": [],
    },
    {
        "id": "pdf_to_text",
        "label": "PDF → Text",
        "description": "Extract all text from a PDF document",
        "icon": "FileText",
        "input_mode": "file",
        "file_types": ["pdf"],
        "options": [],
    },
    {
        "id": "text_to_summary",
        "label": "Text → Summary",
        "description": "Condense text into a concise summary using BART",
        "icon": "AlignLeft",
        "input_mode": "text_or_file",
        "file_types": ["txt"],
        "options": [],
    },
    {
        "id": "text_to_translation",
        "label": "Text → Translation",
        "description": "Translate English text to another language",
        "icon": "Languages",
        "input_mode": "text_or_file",
        "file_types": ["txt"],
        "options": [
            {
                "key": "target_language",
                "label": "Target Language",
                "type": "select",
                "choices": ["French", "Spanish", "German", "Italian", "Portuguese", "Dutch", "Russian", "Chinese", "Japanese", "Arabic"],
                "default": "French",
            }
        ],
    },
    {
        "id": "text_to_pdf",
        "label": "Text → PDF",
        "description": "Format and export text as a PDF document",
        "icon": "FileOutput",
        "input_mode": "text_or_file",
        "file_types": ["txt"],
        "options": [],
    },
    {
        "id": "text_to_audio",
        "label": "Text → Audio",
        "description": "Convert text to natural speech audio",
        "icon": "Volume2",
        "input_mode": "text_or_file",
        "file_types": ["txt"],
        "options": [],
    },
]

CONVERTER_MAP = {
    "audio_to_text": AudioToText,
    "image_to_caption": ImageToCaption,
    "image_to_pdf": ImageToPDF,
    "image_to_text": ImageToText,
    "pdf_to_text": PDFToText,
    "text_to_audio": TextToAudio,
    "text_to_pdf": TextToPDF,
    "text_to_summary": TextToSummary,
    "text_to_translation": TextToTranslation,
}

class ConversionRouter:
    def Convert(self, conversion_type: str, file_bytes: bytes = None, text_input: str = None, options: dict = None) -> dict:
        try:
            logger.info("Routing conversion: %s", conversion_type)
            if conversion_type not in CONVERTER_MAP:
                raise KeyError(conversion_type)
            result = CONVERTER_MAP[conversion_type]().Convert(
                file_bytes=file_bytes,
                text_input=text_input,
                options=options or {}
            )
            logger.info("Conversion successful: %s", conversion_type)
            return result
        except Exception:
            logger.error("ConversionRouter failed for type '%s'", conversion_type, exc_info=True)
            raise