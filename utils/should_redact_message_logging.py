
def should_redact_message_logging(model_call_details: dict) -> bool:
    """
    Determine if message logging should be redacted.

    Priority order:
    1. Dynamic parameter (turn_off_message_logging in request)
    2. Headers (litellm-disable-message-redaction / litellm-enable-message-redaction)
    3. Global setting (litellm.turn_off_message_logging)
    """
    litellm_params = model_call_details.get("litellm_params", {})

    metadata_field = get_metadata_variable_name_from_kwargs(litellm_params)
    metadata = litellm_params.get(metadata_field, {})
    if not isinstance(metadata, dict):
        # Fall back: litellm_metadata was None, try metadata
        metadata = litellm_params.get("metadata", {})
    if not isinstance(metadata, dict):
        metadata = {}

    # Get headers from the metadata
    request_headers = metadata.get("headers", {})

    # Check for headers that explicitly control redaction
    if request_headers and bool(
        request_headers.get("litellm-disable-message-redaction", False)
    ):
        # User explicitly disabled redaction via header
        return False

    possible_enable_headers = [
        "litellm-enable-message-redaction",  # old header. maintain backwards compatibility
        "x-litellm-enable-message-redaction",  # new header
    ]

    is_redaction_enabled_via_header = False
    for header in possible_enable_headers:
        if bool(request_headers.get(header, False)):
            is_redaction_enabled_via_header = True
            break

    # Priority 1: Check dynamic parameter first (if explicitly set)
    dynamic_turn_off = _get_turn_off_message_logging_from_dynamic_params(
        model_call_details
    )
    if dynamic_turn_off is not None:
        # Dynamic parameter is explicitly set, use it
        return dynamic_turn_off

    # Priority 2: Check if header explicitly enables redaction
    if is_redaction_enabled_via_header:
        return True

    # Priority 3: Fall back to global setting
    return litellm.turn_off_message_logging is True

