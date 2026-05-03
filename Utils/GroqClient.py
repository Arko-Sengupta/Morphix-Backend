import os
import logging
from groq import Groq
from dotenv import load_dotenv

load_dotenv(".env")
logger = logging.getLogger(__name__)

class GroqClient:
    def __init__(self):
        token = os.getenv("GROQ_API_KEY")
        if not token:
            raise ValueError("GROQ_API_KEY not found in environment variables.")
        self.client = Groq(api_key=token)
        logger.info("GroqClient initialized")