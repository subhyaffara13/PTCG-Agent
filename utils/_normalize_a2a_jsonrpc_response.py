from typing import Any, Dict, Optional

def _normalize_a2a_jsonrpc_response(
    response_dict: Dict[str, Any],
    request_id: Optional[Any] = None,
) -> Dict[str, Any]:
    """
    Ensure JSON-RPC responses include ``id`` when the caller supplied one.

    The a2a SDK may omit ``id`` on error payloads even when the upstream agent
    returned it. Backfill from the outbound request id so LiteLLM can surface the
    agent error instead of failing Pydantic validation.
    """
    normalized = dict(response_dict)
    if normalized.get("id") is None and request_id is not None:
        normalized["id"] = str(request_id)
    return normalized

