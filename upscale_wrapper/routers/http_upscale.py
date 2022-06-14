"""Upscale endpoints"""
import cv2
from fastapi import APIRouter, HTTPException, UploadFile, Response
from upscale_wrapper.logger import LoggerSetup
from upscale_wrapper.lib.upscale import get_models, upscale_img
import io
import numpy as np
from time import time


# ------------------------------ Initialization -------------------------------
router = APIRouter()
LOGGER = LoggerSetup(__name__, "info").get_minimal()
MODELS = get_models()

@router.post(
    "/api/upscale/",
    response_model=dict,
    status_code=200
)
async def upscale_image(
    model: str,
    image: UploadFile,
    multiplier: int,
    resize: bool = False,
):
    try:
        upscale_model = None 
        # Find the model
        for item in MODELS:
            if item["model_name"].lower() == model.lower() and item["model_multiplier"] == multiplier:
                upscale_model = item["model"]
                break

        # If no model is found raise exception.
        if not upscale_model:
            raise HTTPException(status_code=404, detail="Model not found!")
        
        # Preprocessing the image
        s = time()
        contents = await image.read()
        nparr = np.fromstring(contents, np.uint8)
        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        e = time()
        print(f"preprocessing time {(e - s) * 1000} ms")


        s = time()
        # Upscale the image
        image = upscale_img(
            model=upscale_model,
            image=image,
            resize=resize
        )
        e = time()
        print(f"upscaling time {(e - s) * 1000} ms")

        s = time()
        _, image = cv2.imencode(".png", image)
        e = time()
        print(f"encode time {(e - s) * 1000} ms")
        # StreamingResponse(
        #     io.BytesIO(image.tobytes()), media_type="image/png")
        return Response(content=image.tobytes(), media_type="image/png")

    except HTTPException as err:
        LOGGER.error(err)
        raise HTTPException(
            status_code=err.status_code,
            detail=err.detail
        ) from err

    except Exception as err:
        LOGGER.error(err)
        raise HTTPException(status_code=400) from err