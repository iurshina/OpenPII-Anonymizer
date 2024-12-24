
from fastapi import APIRouter, HTTPException
from anonymizer.api.schemas import (
    AnonymizeRequest,
    AnonymizeResponse
)
import logging
from anonymizer.llm.azure_llm import anonymize_text, anonymize_text_aware_of_context

logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/anonymize", response_model=AnonymizeResponse)
async def anonymize_route(request: AnonymizeRequest):
    """
    Full pipeline: Detect PII, resolve anaphora, and differentiate public vs. private data.
    Save the input and output to the database.
    """
    try:
        result = anonymize_text(request.input_text)

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

@router.post("/anonymize/context-aware", response_model=AnonymizeResponse)
async def anonymize_context_aware_route(request: AnonymizeRequest):
    """
    Context-based anonymization: Detect and anonymize sensitive data with contextual understanding.
    Save the input and output to the database.
    """
    try:
        result = anonymize_text_aware_of_context(request.input_text)

        return {
            "anonymized_text": result.get("anonymized_text", ""),
            "redacted_pii": result.get("redacted_pii", []),
        }
    except Exception as e:
        logger.error(f"An error occurred during context-aware anonymization: {e}", exc_info=True)

        raise HTTPException(
            status_code=500,
            detail={
                "message": "Internal Server Error",
                "error": str(e),
                "hint": "Check the logs for more details.",
            }
        )