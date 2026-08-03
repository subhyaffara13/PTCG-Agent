import re

def _is_valid_ttl_format(ttl: str) -> bool:
    """
    Validate TTL format. Should be a string ending with 's' for seconds.
    Examples: "3600s", "7200s", "1.5s"

    Args:
        ttl: TTL string to validate

    Returns:
        bool: True if valid format, False otherwise
    """
    if not isinstance(ttl, str):
        return False

    # TTL should end with 's' and contain a valid number before it
    pattern = r"^([0-9]*\.?[0-9]+)s$"
    match = re.match(pattern, ttl)

    if not match:
        return False

    try:
        # Ensure the numeric part is valid and positive
        numeric_part = float(match.group(1))
        return numeric_part > 0
    except ValueError:
        return False

