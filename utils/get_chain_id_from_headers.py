from typing import Dict, Optional

def get_chain_id_from_headers(headers: Optional[Dict[str, str]]) -> Optional[str]:
    """
    Extract chain id for call chaining from request headers.

    Priority order:
    1. ``x-litellm-trace-id`` (explicit, highest priority)
    2. ``x-litellm-session-id`` (explicit)
    3. Any ``x-<vendor>-session-id`` header whose value looks like a session id
       (alphanumeric / UUID, at least 8 chars).  E.g. ``x-claude-code-session-id``.

    Header keys are matched case-insensitively so this works with raw header
    dicts from any transport.

    Used by MCP (and other paths that have raw_headers but no Request) to set
    litellm_trace_id/litellm_session_id for spend logs and logging consistency.
    """
    if not headers:
        return None
    normalized = {k.lower(): v for k, v in headers.items() if isinstance(k, str)}
    return (
        normalized.get("x-litellm-trace-id")
        or normalized.get("x-litellm-session-id")
        or _extract_generic_session_id_from_headers(normalized)
    )

