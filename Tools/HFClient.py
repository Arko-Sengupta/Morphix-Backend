import os
import logging
import requests
from dotenv import load_dotenv

load_dotenv(".env")
logger = logging.getLogger(__name__)

class HFClient:
    def __init__(self):
        try:
            self.base_url = os.getenv("HF_API_URL", "https://router.huggingface.co/hf-inference/models/")
            self.token = os.getenv("HF_API_TOKEN")
            if not self.token:
                raise ValueError("HF_API_TOKEN not found in environment variables.")
            self.headers = {"Authorization": f"Bearer {self.token}"}
            logger.info("HFClient initialized")
        except Exception:
            logger.error("Failed to initialize HFClient", exc_info=True)
            raise

    def Call(self, model_id: str, *, json_payload: dict = None, binary_payload: bytes = None, content_type: str = "application/octet-stream") -> requests.Response:
        try:
            logger.info("Calling HF model: %s", model_id)
            url = f"{self.base_url}{model_id}"
            headers = dict(self.headers)
            if binary_payload is not None:
                headers["Content-Type"] = content_type
                response = requests.post(url, headers=headers, data=binary_payload, timeout=180)
            else:
                response = requests.post(url, headers=headers, json=json_payload, timeout=180)
            response.raise_for_status()
            return response
        except requests.HTTPError as e:
            logger.error("HF API HTTP error for model %s: %s", model_id, response.text, exc_info=True)
            raise RuntimeError(f"HF API error ({response.status_code}): {response.text}") from e
        except Exception:
            logger.error("HF API call failed for model %s", model_id, exc_info=True)
            raise