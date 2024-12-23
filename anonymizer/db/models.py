from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func

Base = declarative_base()

class LLMCall(Base):
    """
    Database model for storing LLM call inputs and outputs.
    """
    __tablename__ = "llm_calls"

    id = Column(Integer, primary_key=True, index=True)
    input_text = Column(Text, nullable=False)  
    output_text = Column(Text, nullable=False)  
    pii_types = Column(String, nullable=True) 
    created_at = Column(DateTime(timezone=True), server_default=func.now()) 

    def __repr__(self):
        return f"<LLMCall(id={self.id}, created_at={self.created_at})>"
