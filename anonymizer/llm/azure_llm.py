import openai
from anonymizer.utils.config import settings

AZURE_API_KEY = settings.AZURE_API_KEY
AZURE_ENDPOINT = settings.AZURE_ENDPOINT 
AZURE_ENGINE = settings.AZURE_ENGINE    
AZURE_API_VERSION = settings.AZURE_API_VERSION

openai.api_type = "azure"
openai.azure_endpoint = AZURE_ENDPOINT
openai.api_version = AZURE_API_VERSION
openai.api_key = AZURE_API_KEY

def call_azure_llm(prompt: str, engine: str = AZURE_ENGINE, max_tokens: int = 1000) -> str:
    """
    Calls Azure OpenAI with the provided prompt.
    """
    try:
        response = openai.Completion.create(
            engine=engine,
            prompt=prompt,
            max_tokens=max_tokens,
            temperature=0.7,
        )
        return response.choices[0].text.strip()
    except Exception as e:
        print(f"Error calling Azure LLM: {e}")
        return ""

# Step 1: PII Detection
def detect_pii(input_text: str) -> list:
    from anonymizer.llm.prompts import PII_DETECTION_PROMPT

    prompt = PII_DETECTION_PROMPT.format(text=input_text)
    response = call_azure_llm(prompt)
    try:
        pii_list = eval(response)
        return pii_list
    except Exception as e:
        print(f"Error parsing PII detection response: {e}")
        return []

# Step 2: Anaphora Resolution
def resolve_anaphora(input_text: str, pii_data: list) -> dict:
    from anonymizer.llm.prompts import ANAPHORA_RESOLUTION_PROMPT

    prompt = ANAPHORA_RESOLUTION_PROMPT.format(input_text=input_text, pii_data=pii_data)
    response = call_azure_llm(prompt)
    try:
        resolved_data = eval(response)
        return resolved_data
    except Exception as e:
        print(f"Error parsing anaphora resolution response: {e}")
        return {"resolved_text": input_text, "entities": []}

# Step 3: Public-Interest vs. PII Differentiation
def differentiate_public_interest(resolved_text: str) -> dict:
    from anonymizer.llm.prompts import INFO_CLASSIFICATION_PROMPT
    
    prompt = INFO_CLASSIFICATION_PROMPT.format(input_text=resolved_text)
    response = call_azure_llm(prompt)
    try:
        result = eval(response)
        return result
    except Exception as e:
        print(f"Error parsing public-interest response: {e}")
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