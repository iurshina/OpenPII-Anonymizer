PII_DETECTION_PROMPT = """
    Identify and classify all personally identifiable information (PII) in the following text.
    Return the results in the format: [{"type": "<PII type>", "value": "<PII value>"}].

    Text:
    {input_text}
    """

ANAPHORA_RESOLUTION_PROMPT = """
    Track references to entities in the following text and assign consistent placeholders. Use the PII information provided below for placeholders.
    Ensure that all references (e.g., pronouns like "he," "she") resolve to the correct placeholder.

    Return the output in the format:
    {
    "resolved_text": "<text with placeholders>",
    "entities": [{"placeholder": "<Placeholder>", "original": "<Original>", "type": "<PII type>"}]
    }.

    For example:
    Input: "John lives in New York. He works there."
    PII: [{"type": "PERSON", "value": "John"}, {"type": "LOCATION", "value": "New York"}]
    Output: {
    "resolved_text": "<Person 1> lives in <Location 1>. <Person 1> works in <Location 1>.",
    "entities": [
        {"placeholder": "<Person 1>", "original": "John", "type": "PERSON"},
        {"placeholder": "<Location 1>", "original": "New York", "type": "LOCATION"}
    ]
    }.

    Text:
    {input_text}
    PII:
    {pii_data}
    """

INFO_CLASSIFICATION_PROMPT = """
    Differentiate between public-interest information and PII in the following text with placeholders.
    Redact only the private PII while retaining public-interest information.

    Return the final anonymized text in the format:
    {
    "anonymized_text": "<text with PII redacted>",
    "public_info": [{"text": "<retained public-interest text>", "start": <start index>, "end": <end index>}]
    }.

    For example:
    Input: "<Person 1> lives in <Location 1>. The library on Main Street is <PUBLIC>."
    Output: {
    "anonymized_text": "<Person 1> lives in <Location 1>. The library on Main Street is <PUBLIC>.",
    "public_info": [{"text": "The library on Main Street", "start": 30, "end": 55}]
    }.

    Text:
    {input_text}
    """
