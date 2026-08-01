
def extract_provider_resource_id_from_unified_id(
    unified_id: str,
) -> Optional[str]:
    """
    Extract provider resource ID from a unified resource ID.

    Args:
        unified_id: The unified resource ID (decoded or encoded)

    Returns:
        Provider resource ID string or None

    Example:
        unified_id = "litellm_proxy:vector_store;...;resource_id,vs_abc123;..."
        returns: "vs_abc123"
    """
    try:
        # Ensure unified_id is a string
        if not isinstance(unified_id, str):
            return None

        # Decode if it's base64 encoded
        decoded_id = is_base64_encoded_unified_id(unified_id)
        if decoded_id:
            unified_id = decoded_id

        # Extract resource ID (try multiple patterns for different resource types)
        patterns = [
            r"resource_id,([^;]+)",
            r"vector_store_id,([^;]+)",
            r"file_id,([^;]+)",
        ]

        for pattern in patterns:
            match = re.search(pattern, unified_id)
            if match:
                return match.group(1).strip()

        return None
    except Exception:
        return None

