
"""Document processor Endpoint."""
from fastapi import APIRouter, HTTPException, Query
from upscale_wrapper.logger import LoggerSetup


# ------------------------------ Initialization -------------------------------
router = APIRouter()
logger = LoggerSetup(__name__, "debug").get_minimal()

@router.post(
    "/api/",
    response_model=dict,
)
async def process_document():
    try:

        res = {"message": "Success."}

        return res

    except HTTPException as err:
        logger.error(err)
        raise HTTPException(status_code=400) from err

    except Exception as err:
        logger.error(err)
        raise HTTPException(status_code=400) from err