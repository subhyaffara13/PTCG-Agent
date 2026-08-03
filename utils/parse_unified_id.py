from typing import Optional

def parse_unified_id(
    unified_id: str,
) -> Optional[dict]:
    """
    Parse a unified ID into its components.

    Args:
        unified_id: The unified ID (encoded or decoded)

    Returns:
        Dictionary with parsed components or None if invalid

    Example:
        {
            "resource_type": "vector_store",
            "unified_uuid": "abc-123",
            "target_model_names": ["gpt-4", "gemini"],
            "provider_resource_id": "vs_xyz",
            "model_id": "model-id-123"
        }
    """
    try:
        # Decode if needed
        decoded_id = decode_unified_id(unified_id)
        if not decoded_id:
            # Maybe it's already decoded
            if unified_id.startswith("litellm_proxy:"):
                decoded_id = unified_id
            else:
                return None

        return {
            "resource_type": extract_resource_type_from_unified_id(decoded_id),
            "unified_uuid": extract_unified_uuid_from_unified_id(decoded_id),
            "target_model_names": extract_target_model_names_from_unified_id(
                decoded_id
            ),
            "provider_resource_id": extract_provider_resource_id_from_unified_id(
                decoded_id
            ),
            "model_id": extract_model_id_from_unified_id(decoded_id),
        }
    except Exception:
        return None

