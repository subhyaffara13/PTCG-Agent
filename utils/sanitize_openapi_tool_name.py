
def sanitize_openapi_tool_name(raw_name: str) -> str:
    """Map an OpenAPI operationId / fallback to a provider-safe tool name.

    Replaces any character outside ``[a-zA-Z0-9_-]`` with ``_`` and caps the
    result at 128 chars (the most restrictive of the major providers).
    Lowercased to match the existing convention in
    ``register_tools_from_openapi``.
    """
    if not raw_name:
        return raw_name
    sanitized = _OPENAPI_TOOL_NAME_INVALID_CHARS.sub("_", raw_name).lower()
    return sanitized[:_OPENAPI_TOOL_NAME_MAX_LEN]

