
def _basic_sanitize_anthropic_tool_name(name: str) -> str:
    """Lossy: replace [^a-zA-Z0-9_-] with '_' and truncate to 128.

    Used as a candidate generator for the per-request forward map.
    Callers should NOT use this directly for translation -- always go
    through the forward map so collisions are resolved.
    """
    if not isinstance(name, str) or not name:
        return name
    return _ANTHROPIC_TOOL_NAME_INVALID_CHARS.sub("_", name)[
        :_ANTHROPIC_TOOL_NAME_MAX_LEN
    ]

