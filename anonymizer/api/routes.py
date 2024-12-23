
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from anonymizer.api.schemas import (
    AnonymizeRequest,
    AnonymizeResponse
)
import logging
from anonymizer.llm.azure_llm import anonymize_text
from anonymizer.db.database import SessionLocal
from anonymizer.db.queries import save_llm_call

logger = logging.getLogger(__name__)

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/anonymize", response_model=AnonymizeResponse)
async def anonymize_route(request: AnonymizeRequest, db: Session = Depends(get_db)):
    """
    Full pipeline: Detect PII, resolve anaphora, and differentiate public vs. private data.
    Save the input and output to the database.
    """
    try:
        result = anonymize_text(request.input_text)

        # Save input and output to the database
        save_llm_call(
            session=db,
            input_text=request.input_text,
            output_text=result["anonymized_text"],
            pii_types=request.pii_types
        )

        return {
            "anonymized_text": result["anonymized_text"],
            "redacted_pii": [entity["original"] for entity in result["resolved_entities"]],
        }
    except Exception as e:
        logger.error(f"An error occurred during anonymization: {e}", exc_info=True)

        raise HTTPException(
            status_code=500,
            detail={
                "message": "Internal Server Error",
                "error": str(e),  
                "hint": "Check the logs for more details.",
            }
        )