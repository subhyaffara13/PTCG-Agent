from typing import Any, Dict, Optional

def get_session_id_from_a2a_params(params: Dict[str, Any]) -> Optional[str]:
    message = params.get("message", {})
    if isinstance(message, dict):
        return message.get("contextId")
    return getattr(message, "contextId", None)

