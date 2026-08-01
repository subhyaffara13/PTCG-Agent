
def _get_base64_size(base64_str: str) -> int:
    """Estimate the byte size of a base64-encoded string."""
    # Remove any prefix like "data:image/png;base64,"
    if "," in base64_str:
        base64_str = base64_str.split(",")[1]

    padding = 0
    if base64_str.endswith("=="):
        padding = 2
    elif base64_str.endswith("="):
        padding = 1

    return (len(base64_str) * 3) // 4 - padding

