
def _get_web_search_requests(server_tool_use: Any) -> Optional[int]:
    """
    Tolerantly read ``web_search_requests`` from a ``server_tool_use`` value
    that may be ``None``, a ``dict``, a ``ServerToolUse`` pydantic instance,
    or any other object supporting attribute access.

    Returns ``None`` when the value cannot be resolved — callers can
    distinguish "absent" from "zero" using ``is None``.

    See https://github.com/BerriAI/litellm/issues/26153 — ``stream_chunk_builder``
    historically left this as a plain ``dict``, which broke direct attribute
    access in cost calculation.
    """
    if server_tool_use is None:
        return None
    if isinstance(server_tool_use, dict):
        return server_tool_use.get("web_search_requests")
    return getattr(server_tool_use, "web_search_requests", None)

