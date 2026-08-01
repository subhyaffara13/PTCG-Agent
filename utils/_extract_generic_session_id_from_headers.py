
def _extract_generic_session_id_from_headers(
    normalized: Dict[str, str],
) -> Optional[str]:
    """
    Scan a normalised (lower-cased keys) header dict for any header that looks
    like ``x-<vendor>-session-id`` and whose value is a plausible session/trace
    identifier (alphanumeric + hyphens/underscores, at least 8 chars).

    The two explicit LiteLLM headers (``x-litellm-trace-id`` /
    ``x-litellm-session-id``) are excluded here because they are handled with
    higher priority by the caller.

    Example: ``x-claude-code-session-id: e96634a3-fa28-4083-b354-55542e2dca01``
    """
    for key, value in normalized.items():
        if (
            key not in _EXPLICIT_SESSION_HEADERS
            and _GENERIC_SESSION_ID_HEADER_RE.match(key)
            and isinstance(value, str)
            and _SESSION_ID_VALUE_RE.match(value)
        ):
            return value
    return None

