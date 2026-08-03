import time

def _safe_convert_created_field(created_value) -> int:
    """
    Safely convert a 'created' field value to an integer.

    Some providers (like SambaNova) return the 'created' field as a float
    (Unix timestamp with fractional seconds), but LiteLLM expects an integer.

    Args:
        created_value: The value from response_object["created"]

    Returns:
        int: Unix timestamp as integer
    """
    if created_value is None:
        return int(time.time())
    elif isinstance(created_value, int):
        return created_value
    elif isinstance(created_value, float):
        return int(created_value)
    else:
        # for strings, etc
        try:
            return int(float(created_value))
        except (ValueError, TypeError):
            # Fallback to current time if conversion fails
            return int(time.time())

