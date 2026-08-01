
def decode_unified_id(encoded_unified_id: str) -> Optional[str]:
    """
    Decode a base64 encoded unified ID.

    Args:
        encoded_unified_id: The base64 encoded unified ID

    Returns:
        Decoded unified ID string or None if invalid
    """
    try:
        # Add padding back if needed
        padded = encoded_unified_id + "=" * (-len(encoded_unified_id) % 4)

        # Decode from base64
        decoded = base64.urlsafe_b64decode(padded).decode()

        # Verify it starts with the expected prefix
        if decoded.startswith("litellm_proxy:"):
            return decoded

        return None
    except Exception:
        return None

