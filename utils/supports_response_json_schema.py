import re

def supports_response_json_schema(model: str) -> bool:
    """
    Check if the model supports responseJsonSchema (JSON Schema format).

    responseJsonSchema is supported by Gemini 2.0+ models and uses standard
    JSON Schema format with lowercase types (string, object, etc.) instead of
    the OpenAPI-style responseSchema with uppercase types (STRING, OBJECT, etc.).

    Benefits of responseJsonSchema:
    - Supports additionalProperties for stricter schema validation
    - Uses standard JSON Schema format (no type conversion needed)
    - Better compatibility with Pydantic's model_json_schema()

    Args:
        model: The model name (e.g., "gemini-2.0-flash", "gemini-2.5-pro")

    Returns:
        True if the model supports responseJsonSchema, False otherwise
    """
    model_lower = model.lower()

    # Gemini 2.0+ and 2.5+ models support responseJsonSchema
    # Pattern matches: gemini-2.0-*, gemini-2.5-*, gemini-3-*, etc.
    gemini_2_plus_pattern = re.compile(r"gemini-(?:[2-9]|[1-9]\d+)(?:\.|\-)")

    return bool(gemini_2_plus_pattern.search(model_lower))

