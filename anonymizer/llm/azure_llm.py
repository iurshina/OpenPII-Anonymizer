from openai import AzureOpenAI
import json

from anonymizer.utils.config import settings
from anonymizer.utils.logger import setup_logger
from anonymizer.db.queries import save_llm_call
from anonymizer.db.database import SessionLocal
from anonymizer.db.models import PromptType

logger = setup_logger("azure_llm")

AZURE_API_KEY = settings.AZURE_API_KEY
AZURE_ENDPOINT = settings.AZURE_ENDPOINT 
AZURE_ENGINE = settings.AZURE_ENGINE    
AZURE_API_VERSION = settings.AZURE_API_VERSION

client = AzureOpenAI(
    api_version=AZURE_API_VERSION,  
    azure_endpoint=AZURE_ENDPOINT,
    api_key=AZURE_API_KEY
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def call_azure_llm(prompt: str, engine: str = AZURE_ENGINE, max_tokens: int = 1000) -> str:
    """
    Calls Azure OpenAI with the provided prompt.
    """
    try:
        response = client.chat.completions.create(
            model=engine,  
            messages=[
                {"role": "system", "content": "You are an assistant that identifies and anonymizes PII."}, 
                {"role": "user", "content": prompt}, 
            ],
            max_tokens=max_tokens
        )

        response_dict = response.to_dict()

        return response_dict["choices"][0]["message"]["content"]
    except Exception as e:
        logger.error(f"Error calling Azure LLM: {e}")
        raise

# Step 1: PII Detection
def detect_pii(input_text: str) -> list:
    from anonymizer.llm.prompts import PII_DETECTION_PROMPT

    prompt = PII_DETECTION_PROMPT.format(input_text=input_text)
    
    response = call_azure_llm(prompt)
    logger.debug(f"Raw Response: {response}")

    db = next(get_db())
    save_llm_call(
        session=db,
        prompt_type=PromptType.PII_DETECTION,
        prompt=prompt,
        output=response
    )

    try:
        pii_list = json.loads(response)
        return pii_list
    except Exception as e:
        logger.error(f"Error parsing PII detection response: {e}", exc_info=True)
        return []

# Step 2: Anaphora Resolution
def resolve_anaphora(input_text: str, pii_data: list) -> dict:
    from anonymizer.llm.prompts import ANAPHORA_RESOLUTION_PROMPT

    prompt = ANAPHORA_RESOLUTION_PROMPT.format(input_text=input_text, pii_data=pii_data)
    
    response = call_azure_llm(prompt)
    logger.debug(f"Raw Response: {response}")

    db = next(get_db())
    save_llm_call(
        session=db,
        prompt_type=PromptType.ANAPHORA_RESOLUTION,
        prompt=prompt,
        output=response
    )

    try:
        resolved_data = json.loads(response)
        return resolved_data
    except Exception as e:
        logger.error(f"Error parsing anaphora resolution response: {e}", exc_info=True)
        return {"resolved_text": input_text, "entities": []}

# Step 3: Public-Interest vs. PII Differentiation
def differentiate_public_interest(resolved_text: str) -> dict:
    from anonymizer.llm.prompts import INFO_CLASSIFICATION_PROMPT

    prompt = INFO_CLASSIFICATION_PROMPT.format(input_text=resolved_text)
    
    response = call_azure_llm(prompt)
    logger.debug(f"Raw Response: {response}")

    db = next(get_db())
    save_llm_call(
        session=db,
        prompt_type=PromptType.PUBLIC_INTEREST_DIFFERENTIATION,
        prompt=prompt,
        output=response
    )

    try:
        result = json.loads(response)
        return result
    except Exception as e:
        logger.error(f"Error parsing public-interest response: {e}", exc_info=True)
        return {"anonymized_text": resolved_text, "public_info": []}

def anonymize_text(input_text: str) -> dict:
    """
    Combines all steps to produce final anonymized text.
    """
    pii_data = detect_pii(input_text)
    
    resolved_data = resolve_anaphora(input_text, pii_data)
    resolved_text = resolved_data["resolved_text"]
    
    final_result = differentiate_public_interest(resolved_text)
    
    return {
        "anonymized_text": final_result["anonymized_text"],
        "public_info": final_result["public_info"],
        "resolved_entities": resolved_data["entities"]
    }

def anonymize_text_aware_of_context(input_text: str):
    from anonymizer.llm.prompts import CONTEXT_AWARE_ANONYMIZATION_PROMPT

    prompt = CONTEXT_AWARE_ANONYMIZATION_PROMPT.format(input_text=input_text)
    
    response = call_azure_llm(prompt)
    logger.debug(f"Raw Response: {response}")

    db = next(get_db())
    save_llm_call(
        session=db,
        prompt_type=PromptType.CONTEXT_BASED_REPHRASING,
        prompt=prompt,
        output=response
    )

    try:
        result = json.loads(response)
        return result
    except Exception as e:
        logger.error(f"Error parsing context-aware rephrasing response: {e}", exc_info=True)
        return {}