
def extract_resource_type_from_unified_id(
    unified_id: str,
) -> Optional[str]:
    """
    Extract resource type from a unified resource ID.

    Args:
        unified_id: The unified resource ID (decoded or encoded)

    Returns:
        Resource type string or None

    Example:
        unified_id = "litellm_proxy:vector_store;unified_id,uuid;..."
        returns: "vector_store"
    """
    try:
        # Ensure unified_id is a string
        if not isinstance(unified_id, str):
            return None

        # Decode if it's base64 encoded
        decoded_id = is_base64_encoded_unified_id(unified_id)
        if decoded_id:
            unified_id = decoded_id

        # Extract resource type (comes after prefix and before first semicolon)
        match = re.search(r"litellm_proxy:([^;]+)", unified_id)
        if match:
            return match.group(1).strip()

        return None
    except Exception:
        return None

