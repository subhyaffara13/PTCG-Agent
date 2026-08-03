from typing import Any, Optional

def get_chatgpt_session_id(litellm_params: Optional[Any]) -> Optional[str]:
    params = _normalize_litellm_params(litellm_params)
    for key in ("litellm_session_id", "session_id"):
        value = params.get(key)
        if value:
            return str(value)
    metadata = params.get("metadata")
    if isinstance(metadata, dict):
        value = metadata.get("session_id")
        if value:
            return str(value)
    for key in ("litellm_trace_id", "litellm_call_id"):
        value = params.get(key)
        if value:
            return str(value)
    return None

