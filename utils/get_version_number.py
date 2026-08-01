
def get_version_number(prompt_id: str) -> int:
    """
    Extract the version number from a versioned prompt ID.

    Args:
        prompt_id: Prompt ID that may include version suffix (e.g., "jack_success.v2" or "jack_success_v2")

    Returns:
        Version number (defaults to 1 if no version suffix or invalid format)

    Examples:
        >>> get_version_number("jack_success.v2")
        2
        >>> get_version_number("jack_success_v2")
        2
        >>> get_version_number("jack_success")
        1
    """
    # Try dot separator first (.v)
    if ".v" in prompt_id:
        version_str = prompt_id.split(".v")[1]
        try:
            return int(version_str)
        except ValueError:
            pass

    # Try underscore separator (_v)
    if "_v" in prompt_id:
        version_str = prompt_id.split("_v")[1]
        try:
            return int(version_str)
        except ValueError:
            pass

    return 1

