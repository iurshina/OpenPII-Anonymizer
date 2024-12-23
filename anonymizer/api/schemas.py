from pydantic import BaseModel
from enum import Enum
from typing import List


class PIIType(str, Enum):
    PERSON = "person"
    ORGANIZATION = "organization"
    LOCATION = "location"
    PHONE = "phone"
    EMAIL = "email"

class AnonymizeRequest(BaseModel):
    input_text: str  
    pii_types: List[PIIType]  

class AnonymizeResponse(BaseModel):
    anonymized_text: str  
    redacted_pii: List[str]  
