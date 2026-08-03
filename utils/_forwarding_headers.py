from typing import Dict, Optional

def _forwarding_headers(
    user_api_key_dict: UserAPIKeyAuth,
    request_data: dict,
    agent_extra_headers: Optional[Dict[str, str]],
) -> Optional[Dict[str, str]]:
    sanitized = (
        {
            k: v
            for k, v in agent_extra_headers.items()
            if not k.lower().startswith("x-litellm-")
        }
        if agent_extra_headers
        else None
    )
    merged = merge_agent_headers(dynamic_headers=sanitized, static_headers=None) or {}
    identity = _caller_identity_headers(user_api_key_dict)
    trace_id = request_data.get("litellm_trace_id")
    if trace_id:
        identity["X-LiteLLM-Trace-Id"] = str(trace_id)
    merged.update(identity)
    return merged or None

