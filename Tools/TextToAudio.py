import os
import base64
import asyncio
import logging
import tempfile
import edge_tts
import concurrent.futures
from dotenv import load_dotenv

load_dotenv(".env")
logger = logging.getLogger(__name__)

class TextToAudio:
    def __init__(self):
        self.voice = os.getenv("EDGE_TTS_VOICE", "en-US-JennyNeural")
        logger.info("TextToAudio initialized with voice: %s", self.voice)

    def Convert(self, file_bytes: bytes = None, text_input: str = None, options: dict = None) -> dict:
        try:
            logger.info("Starting TextToAudio conversion")
            text = text_input or (file_bytes.decode("utf-8", errors="replace") if file_bytes else "")
            with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
                audio_bytes = executor.submit(asyncio.run, self._synthesize(text)).result()
            logger.info("TextToAudio conversion successful")
            return {
                "type": "binary",
                "content": base64.b64encode(audio_bytes).decode(),
                "filename": "speech.mp3",
                "mime_type": "audio/mpeg",
            }
        except Exception:
            logger.error("TextToAudio conversion failed", exc_info=True)
            raise

    async def _synthesize(self, text: str) -> bytes:
        with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as f:
            tmp_path = f.name
        try:
            communicate = edge_tts.Communicate(text, voice=self.voice)
            await communicate.save(tmp_path)
            with open(tmp_path, "rb") as f:
                return f.read()
        finally:
            os.unlink(tmp_path)