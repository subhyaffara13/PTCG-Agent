from typing import Any, Dict, Optional

def get_session_id_from_request_data(request_data: Dict[str, Any]) -> Optional[str]:
    """Extract session_id from request data (litellm_session_id or metadata)."""
    session_id = request_data.get("litellm_session_id")
    if session_id:
        return str(session_id)

    metadata = request_data.get("metadata") or {}
    session_id = metadata.get("session_id")
    if session_id:
        return str(session_id)

    litellm_metadata = request_data.get("litellm_metadata") or {}
    session_id = litellm_metadata.get("session_id")
    if session_id:
        return str(session_id)

    return None

