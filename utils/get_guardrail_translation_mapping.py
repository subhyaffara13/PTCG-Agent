
def get_guardrail_translation_mapping(call_type: CallTypes) -> Type["BaseTranslation"]:
    """
    Get the guardrail translation handler for a given call type.

    Args:
        call_type: The type of call (e.g., completion, acompletion, anthropic_messages)

    Returns:
        The translation handler class for the given call type

    Raises:
        ValueError: If no translation mapping exists for the given call type
    """
    global endpoint_guardrail_translation_mappings

    # Lazy load the mappings on first access
    if endpoint_guardrail_translation_mappings is None:
        endpoint_guardrail_translation_mappings = (
            discover_guardrail_translation_mappings()
        )

    # Get the translation handler class for the call type
    if call_type not in endpoint_guardrail_translation_mappings:
        raise ValueError(
            f"No guardrail translation mapping found for call_type: {call_type}. "
            f"Available mappings: {list(endpoint_guardrail_translation_mappings.keys())}"
        )

    # Return the handler class directly
    return endpoint_guardrail_translation_mappings[call_type]

