
def _sanitize_repr_for_diff(x_str: str) -> str:
    """
    Replace memory addresses in an object's repr with a stable placeholder
    so that beautiful JSON diffs won't be ruined by ephemeral addresses.
    """
    return MEMORY_ADDRESS_REGEX.sub("object at 0xXXXXXXXX", x_str)

