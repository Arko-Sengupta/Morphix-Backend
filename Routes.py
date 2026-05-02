import json
import logging

from fastapi.responses import JSONResponse
from fastapi import APIRouter, File, Form, UploadFile
from Model import CONVERSIONS, ConversionRouter

logger = logging.getLogger(__name__)

Router = APIRouter()
ConvRouter = ConversionRouter()

@Router.get("/")
async def HealthCheck():
    try:
        logger.info("Health check requested")
        return {"status": "ok", "version": "2.0.0"}
    except Exception as e:
        logger.error("Health check failed", exc_info=True)
        return JSONResponse(status_code=500, content={"error": str(e)})

@Router.get("/conversions")
async def ListConversions():
    try:
        logger.info("Conversions list requested")
        return CONVERSIONS
    except Exception as e:
        logger.error("Failed to list conversions", exc_info=True)
        return JSONResponse(status_code=500, content={"error": str(e)})

@Router.post("/convert")
async def Convert(
    conversion_type: str = Form(...),
    file: UploadFile = File(None),
    text_input: str = Form(None),
    options: str = Form(None)
):
    try:
        logger.info("Conversion requested: %s", conversion_type)
        file_bytes = await file.read() if file else None
        opts = json.loads(options) if options else {}
        result = ConvRouter.Convert(
            conversion_type,
            file_bytes=file_bytes,
            text_input=text_input,
            options=opts
        )
        return JSONResponse(content=result)
    except KeyError:
        logger.warning("Unknown conversion type: %s", conversion_type)
        return JSONResponse(status_code=400, content={"error": f"Unknown conversion type: {conversion_type}"})
    except Exception as e:
        logger.error("Conversion failed for type '%s'", conversion_type, exc_info=True)
        return JSONResponse(status_code=500, content={"error": str(e)})