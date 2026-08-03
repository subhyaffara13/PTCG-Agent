from typing import Any, Dict, Optional, Set

def _sanitize_inbound_headers(
    headers: Any,
    extra_allowlist: Optional[Set[str]] = None,
) -> Optional[Dict[str, str]]:
    """
    Sanitize inbound headers before passing them to a 3rd party guardrail service.

    - Allowlist: default allowlist + extra_allowlist (from litellm_params.extra_headers); only these have values forwarded.
    - All other headers are included with value "[present]" so the guardrail knows the header existed.
    - Coerces values to str (for JSON serialization).
    """
    if not headers or not isinstance(headers, dict):
        return None

    sanitized: Dict[str, str] = {}
    for k, v in headers.items():
        if k is None:
            continue
        key = str(k)
        if _header_value_allowed(key, extra_allowlist=extra_allowlist):
            try:
                sanitized[key] = str(v)
            except Exception:
                continue
        else:
            sanitized[key] = _HEADER_PRESENT_PLACEHOLDER

    return sanitized or None

