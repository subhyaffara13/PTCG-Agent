
def concatenate_base64_list(base64_strings: List[str]) -> str:
    """
    Concatenates a list of base64-encoded strings.

    Args:
        base64_strings (List[str]): A list of base64 strings to concatenate.

    Returns:
        str: The concatenated result as a base64-encoded string.
    """
    # Decode each base64 string and collect the resulting bytes
    combined_bytes = b"".join(base64.b64decode(b64_str) for b64_str in base64_strings)

    # Encode the concatenated bytes back to base64
    return base64.b64encode(combined_bytes).decode("utf-8")

