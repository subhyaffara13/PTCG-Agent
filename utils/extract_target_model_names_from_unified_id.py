import re
from typing import List

def extract_target_model_names_from_unified_id(
    unified_id: str,
) -> List[str]:
    """
    Extract target model names from a unified resource ID.

    Args:
        unified_id: The unified resource ID (decoded or encoded)

    Returns:
        List of target model names

    Example:
        unified_id = "litellm_proxy:vector_store;unified_id,uuid;target_model_names,gpt-4,gemini-2.0"
        returns: ["gpt-4", "gemini-2.0"]
    """
    try:
        # Ensure unified_id is a string
        if not isinstance(unified_id, str):
            return []

        # Decode if it's base64 encoded
        decoded_id = is_base64_encoded_unified_id(unified_id)
        if decoded_id:
            unified_id = decoded_id

        # Extract model names using regex
        match = re.search(r"target_model_names,([^;]+)", unified_id)
        if match:
            # Split on comma and strip whitespace from each model name
            return [model.strip() for model in match.group(1).split(",")]

        return []
    except Exception:
        return []

