import re
from typing import Optional

def extract_unified_uuid_from_unified_id(
    unified_id: str,
) -> Optional[str]:
    """
    Extract the UUID from a unified resource ID.

    Args:
        unified_id: The unified resource ID (decoded or encoded)

    Returns:
        UUID string or None

    Example:
        unified_id = "litellm_proxy:vector_store;unified_id,abc-123;..."
        returns: "abc-123"
    """
    try:
        # Ensure unified_id is a string
        if not isinstance(unified_id, str):
            return None

        # Decode if it's base64 encoded
        decoded_id = is_base64_encoded_unified_id(unified_id)
        if decoded_id:
            unified_id = decoded_id

        # Extract UUID
        match = re.search(r"unified_id,([^;]+)", unified_id)
        if match:
            return match.group(1).strip()

        return None
    except Exception:
        return None

