
def encode_unified_id(unified_id_string: str) -> str:
    """
    Encode a unified ID string to base64.

    Args:
        unified_id_string: The unified ID string to encode

    Returns:
        Base64 encoded unified ID (URL-safe, padding stripped)
    """
    return base64.urlsafe_b64encode(unified_id_string.encode()).decode().rstrip("=")

