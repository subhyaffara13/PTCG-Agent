
def _is_choice_non_empty(choice: Any) -> bool:
    """
    Deep check if a choice contains any meaningful content.

    Args:
        choice: The choice object to check

    Returns:
        bool: True if the choice has meaningful content, False otherwise
    """
    # Check finish_reason
    if hasattr(choice, "finish_reason") and choice.finish_reason is not None:
        return True

    # Check logprobs
    if hasattr(choice, "logprobs") and choice.logprobs is not None:
        return True

    # Check enhancements (if present)
    if hasattr(choice, "enhancements") and choice.enhancements is not None:
        return True

    # Deep check delta object
    if hasattr(choice, "delta") and choice.delta is not None:
        if _is_delta_non_empty(choice.delta):
            return True

    # Check model_extra for dynamically added fields on the choice
    if hasattr(choice, "model_extra") and choice.model_extra:
        for extra_field_name, extra_field_value in choice.model_extra.items():
            # Skip certain structural fields that are just default/None placeholders
            if extra_field_name == "index" and extra_field_value == 0:
                continue
            if (
                extra_field_name in {"finish_reason", "logprobs"}
                and extra_field_value is None
            ):
                continue
            if extra_field_name == "delta":
                continue
            if _has_meaningful_content(extra_field_value):
                return True

    # Check for any other non-standard fields on the choice
    for attr_name in dir(choice):
        # Skip private attributes, methods, and known empty fields
        if (
            attr_name.startswith("_")
            or callable(getattr(choice, attr_name))
            or attr_name.startswith("model_")
            or attr_name
            in {
                "finish_reason",
                "index",
                "delta",
                "logprobs",
                "enhancements",
            }
        ):
            continue

        attr_value = getattr(choice, attr_name, None)
        if _has_meaningful_content(attr_value):
            return True

    return False

