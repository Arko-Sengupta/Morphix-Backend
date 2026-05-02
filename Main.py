import os
import logging

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from dotenv import load_dotenv
from Routes import Router

load_dotenv(".env")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

_default_origins = [
    "http://localhost:5173",
    "http://localhost:5174",
    "http://localhost:5175",
]
_extra = os.getenv("CORS_ORIGINS", "")
_origins = _default_origins + [o.strip() for o in _extra.split(",") if o.strip()]

App = FastAPI(title="Textify Platform", version="2.0.0")
App.add_middleware(
    CORSMiddleware,
    allow_origins=_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)
App.include_router(Router)

if __name__ == "__main__":
    uvicorn.run("Main:App", host="0.0.0.0", port=8000, reload=True)