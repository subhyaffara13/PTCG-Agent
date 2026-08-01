
def is_model_response_stream_empty(model_response: ModelResponseStream) -> bool:
    """
    Check if a ModelResponseStream is empty based on:
    - If finish_reason is set -> it's non empty
    - If any field in choices is set (e.g. content, tool calls, etc.) it's non empty
    - If usage exists -> it's non empty

    This function is robust and ignores fields that are always set (from ModelResponseBase)
    and checks for any meaningful content in other fields.

    Args:
        model_response: The ModelResponseStream to check

    Returns:
        bool: True if the stream is empty, False if it contains meaningful data
    """
    # Fields that are always set in ModelResponseBase and should be ignored
    # These are structural fields that don't indicate content
    BASE_FIELDS = ModelResponseBase.model_fields.keys()

    # Check if usage exists - this indicates meaningful data
    if getattr(model_response, "usage", None) is not None:
        return False

    # Check provider_specific_fields at the top level
    if (
        hasattr(model_response, "provider_specific_fields")
        and model_response.provider_specific_fields is not None
        and model_response.provider_specific_fields != {}
    ):
        return False

    # Check model_extra for dynamically added fields (this is where Pydantic stores them)
    if hasattr(model_response, "model_extra") and model_response.model_extra:
        for extra_field_name, extra_field_value in model_response.model_extra.items():
            if _has_meaningful_content(extra_field_value):
                return False

    # Check for any non-base fields that are set
    # Access model_fields on the class, not the instance, to avoid Pydantic 2.11+ deprecation warnings
    for model_response_field in type(model_response).model_fields.keys():
        # Skip base fields that are always set
        if model_response_field in BASE_FIELDS:
            continue

        # Skip choices - we'll handle them separately with deep inspection
        if model_response_field == "choices":
            continue

        # Check if any other field has meaningful content
        model_response_value = getattr(model_response, model_response_field, None)
        if _has_meaningful_content(model_response_value):
            return False

    # Deep check of choices for any meaningful content
    if hasattr(model_response, "choices") and model_response.choices:
        for choice in model_response.choices:
            if _is_choice_non_empty(choice):
                return False

    # If we get here, the stream is empty
    return True

