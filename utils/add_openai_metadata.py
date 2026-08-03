from typing import Any, Dict, Optional

def add_openai_metadata(
    metadata: Optional[Mapping[str, Any]],
) -> Optional[Dict[str, str]]:
    """
    Add metadata to openai optional parameters, excluding hidden params.

    OpenAI 'metadata' only supports string values.

    Args:
        params (dict): Dictionary of API parameters
        metadata (dict, optional): Metadata to include in the request

    Returns:
        dict: Updated parameters dictionary with visible metadata only
    """
    if metadata is None:
        return None
    # Only include non-hidden parameters
    visible_metadata: Dict[str, str] = {
        str(k): v
        for k, v in metadata.items()
        if k != "hidden_params" and isinstance(v, str)
    }

    # max 16 keys allowed by openai - trim down to 16
    if len(visible_metadata) > 16:
        filtered_metadata = {}
        idx = 0
        for k, v in visible_metadata.items():
            if idx < 16:
                filtered_metadata[k] = v
            idx += 1
        visible_metadata = filtered_metadata

    return visible_metadata.copy()

