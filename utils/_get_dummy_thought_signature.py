
def _get_dummy_thought_signature() -> str:
    """Generate a dummy thought signature for models that require it.

    This is used when transferring conversation history from older models
    (like gemini-2.5-flash) to gemini-3, which requires thought_signature
    for strict validation.
    """
    # Return a base64-encoded dummy signature string
    # Below dummy signature is recommended by google - https://ai.google.dev/gemini-api/docs/thought-signatures#faqs
    dummy_data = b"skip_thought_signature_validator"
    return base64.b64encode(dummy_data).decode("utf-8")

