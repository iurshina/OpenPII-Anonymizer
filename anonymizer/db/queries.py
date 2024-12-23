from .models import LLMCall
from sqlalchemy.orm import Session

def save_llm_call(session: Session, input_text: str, output_text: str, pii_types: list):
    """
    Save an LLM call's input, output, and metadata to the database.
    """
    pii_types_str = ",".join(pii_types) if pii_types else None
    llm_call = LLMCall(input_text=input_text, output_text=output_text, pii_types=pii_types_str)
    session.add(llm_call)
    session.commit()
    session.refresh(llm_call)
    return llm_call