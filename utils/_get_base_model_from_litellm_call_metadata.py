from typing import Optional

def _get_base_model_from_litellm_call_metadata(
    metadata: Optional[dict],
) -> Optional[str]:
    if metadata is None:
        return None
    model_info = metadata.get("model_info")
    if model_info:
        return model_info.get("base_model")
    return None

