from typing import Any, Optional

def ensure_chatgpt_session_id(litellm_params: Optional[Any]) -> str:
    return get_chatgpt_session_id(litellm_params) or str(uuid4())

