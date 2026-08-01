
def is_base64_encoded_unified_id(
    resource_id: str,
    prefix: str = "litellm_proxy:",
) -> Union[str, Literal[False]]:
    """
    Check if a resource ID is a base64 encoded unified ID.

    Args:
        resource_id: The resource ID to check
        prefix: The expected prefix for unified IDs

    Returns:
        Decoded string if valid unified ID, False otherwise
    """
    # Ensure resource_id is a string
    if not isinstance(resource_id, str):
        return False

    # Add padding back if needed
    padded = resource_id + "=" * (-len(resource_id) % 4)

    # Decode from base64
    try:
        decoded = base64.urlsafe_b64decode(padded).decode()
        if decoded.startswith(prefix):
            return decoded
        else:
            return False
    except Exception:
        return False

