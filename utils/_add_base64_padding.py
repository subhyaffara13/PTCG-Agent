
def _add_base64_padding(value: str) -> str:
    """
    Add missing base64 padding when IDs are copied without trailing '=' chars.
    """
    missing_padding = len(value) % 4
    if missing_padding:
        value += "=" * (4 - missing_padding)
    return value

