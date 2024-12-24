from sqlalchemy import Column, Integer, String, Text, DateTime, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
import enum

Base = declarative_base()


class PromptType(enum.Enum):
    """
    Enum to represent the type of LLM prompt.
    """
    PII_DETECTION = "PII Detection"
    ANAPHORA_RESOLUTION = "Anaphora Resolution"
    PUBLIC_INTEREST_DIFFERENTIATION = "Public Interest Differentiation"
    CONTEXT_BASED_REPHRASING = "Contex-based rephrasing"


class LLMCall(Base):
    """
    Database model for storing LLM call inputs and outputs.
    """
    __tablename__ = "llm_calls"

    id = Column(Integer, primary_key=True, index=True)
    prompt_type = Column(Enum(PromptType), nullable=False) 
    prompt = Column(Text, nullable=False)  
    output = Column(Text, nullable=False)  
    created_at = Column(DateTime(timezone=True), server_default=func.now()) 

    def __repr__(self):
        return f"<LLMCall(id={self.id}, prompt_type={self.prompt_type}, created_at={self.created_at})>"
