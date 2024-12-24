PII_DETECTION_PROMPT = """
    Identify and classify all personally identifiable information (PII) in the following text.
    Return the results in the format: [{{"type": "<PII type>", "value": "<PII value>"}}].

    Text:
    {input_text}
"""

ANAPHORA_RESOLUTION_PROMPT = """
    Track references to entities in the following text and assign consistent placeholders. Use the PII information provided below for placeholders.
    Ensure that all references (e.g., pronouns like "he," "she") resolve to the correct placeholder.

    Return the output in the format:
    {{
    "resolved_text": "<text with placeholders>",
    "entities": [{{"placeholder": "<Placeholder>", "original": "<Original>", "type": "<PII type>"}}]
    }}.

    For example:
    Input: "John lives in New York. He works there."
    PII: [{{"type": "PERSON", "value": "John"}}, {{"type": "LOCATION", "value": "New York"}}]
    Output: {{
    "resolved_text": "<Person 1> lives in <Location 1>. <Person 1> works in <Location 1>.",
    "entities": [
        {{"placeholder": "<Person 1>", "original": "John", "type": "PERSON"}},
        {{"placeholder": "<Location 1>", "original": "New York", "type": "LOCATION"}}
    ]
    }}.

    Text:
    {input_text}
    PII:
    {pii_data}
    """

INFO_CLASSIFICATION_PROMPT = """
    Differentiate between public-interest information and PII in the following text with placeholders.
    Redact only the private PII while retaining public-interest information.

    Return the final anonymized text in the format:
    {{
    "anonymized_text": "<text with PII redacted>",
    "public_info": [{{"text": "<retained public-interest text>", "start": <start index>, "end": <end index>}}]
    }}.

    For example:
    Input: "<Person 1> lives in <Location 1>. The library on Main Street is <PUBLIC>."
    Output: {{
    "anonymized_text": "<Person 1> lives in <Location 1>. The library on Main Street is <PUBLIC>.",
    "public_info": [{{"text": "The library on Main Street", "start": 30, "end": 55}}]
    }}.

    Text:
    {input_text}
"""

CONTEXT_AWARE_ANONYMIZATION_PROMPT = """
    ## Instruction Prompt for Context-Aware Anonymization

    ### Task Description:
    You are an AI assistant tasked with **context-aware anonymization** of conversational data. Your goal is to anonymize Personally Identifiable Information (PII) while preserving the **analytical meaning**, **narrative flow**, and **contextual relevance** of the text.

    Focus on **contextual generalization** and **critical data preservation** to protect privacy while ensuring the data remains interpretable and meaningful.

    ---

    ### Key Instructions:

    1. **Identify and Anonymize PII:**
    - Detect and replace the following PII categories:
        - **Names** (e.g., "John" → "Speaker A").
        - **Locations** (e.g., "Paris" → "a major European city").
        - **Relationships** (e.g., "My sister" → "A close relative").
        - **Roles/Professions** (e.g., "I’m a doctor" → "I work in healthcare").
        - **Dates/Timeframes** (e.g., "2012" → "several years ago").
        - **Organizations** (e.g., "Google" → "a large tech company").
        - **Contact Details** (e.g., email addresses or phone numbers → "[REDACTED]").

    - Use **contextual replacements** wherever possible to maintain the original meaning 
        (e.g., "Speaker A works in Berlin" → "Speaker A works in a major city").

    2. **Apply Contextual Generalization:**
    - Generalize details only **when necessary for privacy protection**.
    - Preserve non-sensitive data if critical for understanding or analysis.

        Example:  
        - Original: "I moved to Paris for work."  
        - Generalized: "I moved to a major European city for work."

    3. **Transform Personal Stories:**
    - Replace personal anecdotes with anonymized, generalized versions while retaining relevance to the context.  
        Example:  
        - Original: "My brother and I started a bakery in Munich."  
        - Transformed: "A close relative and I started a small business in a major city."

    4. **Handle Ambiguity:**
    - In cases of ambiguity (e.g., shared names or unclear roles), default to:
        - **Neutral replacements** (e.g., "a person").
        - **Placeholders** (e.g., "[REDACTED]") when context is insufficient for meaningful generalization.

    5. **Preserve Analytical Insights:**
    - Ensure anonymized content reflects the **intent and themes** of the original text without distorting key details or overgeneralizing.

    ---

    ### Input:
    The following text contains PII and needs anonymization:  
    {input_text}

    ---

    ### Output Requirements:

    - Maintain grammatical accuracy and coherence after anonymization.
    - Use square brackets (`[ ]`) for anonymized sections if transparency is needed (e.g., "[Speaker A]").
    - Return content in plain text unless specified otherwise.

    ---

    ### Examples:

    #### Example 1 – Name and Role Anonymization:
    **Input:** "As Peter mentioned earlier, we need to focus on sustainability."  
    **Output:** "As Speaker A mentioned earlier, we need to focus on sustainability."

    #### Example 2 – Location Generalization:
    **Input:** "I grew up in Kirchdorf and later moved to Berlin for work."  
    **Output:** "I grew up in a small village and later moved to a major city for work."

    #### Example 3 – Personal Story Transformation:
    **Input:** "My sister and I started a bakery in Munich, and it has grown significantly."  
    **Output:** "A close relative and I started a small business in a major city, and it has grown significantly."

    ---

    ### Special Notes:

    - When in doubt, prioritize privacy over specificity.
    - Avoid removing critical context that could affect interpretive analysis.
    - For sensitive or ambiguous cases, document assumptions or anonymization decisions.

    ---

    ### Evaluation Criteria:

    1. **Privacy Protection:** Ensure no identifiable information remains.
    2. **Context Retention:** Preserve the original narrative and analytical value.
    3. **Consistency:** Apply anonymization rules uniformly across all examples.
    4. **Accuracy:** Maintain grammatical correctness and semantic coherence.
    """