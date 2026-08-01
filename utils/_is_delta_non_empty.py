
def _is_delta_non_empty(delta: Delta) -> bool:
    """
    Deep check if a delta object contains any meaningful content.

    Args:
        delta: The delta object to check

    Returns:
        bool: True if the delta has meaningful content, False otherwise
    """
    # Check model_extra for dynamically added fields (this is where Pydantic stores them)
    if hasattr(delta, "model_extra") and delta.model_extra:
        for extra_field_name, extra_field_value in delta.model_extra.items():
            # Even structural fields are meaningful if they have actual content
            if _has_meaningful_content(extra_field_value):
                return True

    # Check all regular attributes of the delta object
    for attr_name in dir(delta):
        # Skip private attributes, methods, and Pydantic-specific fields
        if (
            attr_name.startswith("_")
            or callable(getattr(delta, attr_name))
            or attr_name.startswith("model_")
        ):
            continue

        attr_value = getattr(delta, attr_name, None)
        if _has_meaningful_content(attr_value):
            return True

    return False

