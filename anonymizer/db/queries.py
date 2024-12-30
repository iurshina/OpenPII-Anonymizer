from .models import LLMCall
from .models import PromptType
from sqlalchemy.orm import Session

def save_llm_call(session: Session, prompt: str, output: str, prompt_type: PromptType):
    """
    Save an LLM call's input, output, and metadata to the database.
    """
    llm_call = LLMCall(prompt=prompt, output=output, prompt_type=prompt_type)
    session.add(llm_call)
    session.commit()
    session.refresh(llm_call)
    return llm_call