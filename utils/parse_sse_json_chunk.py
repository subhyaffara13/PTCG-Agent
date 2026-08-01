
def parse_sse_json_chunk(chunk: str) -> Optional[Dict[str, Any]]:
    """Parse a single raw SSE line into a JSON object dict.

    Returns ``None`` for empty lines, ``event:`` lines, ``[DONE]`` markers,
    invalid JSON, or non-dict payloads. Centralizes the parsing step that
    feeds into the recovery helpers in this module so behavior stays
    consistent across all callers.
    """
    # Import locally to avoid a circular import with the streaming handler.
    from litellm.litellm_core_utils.streaming_handler import CustomStreamWrapper

    stripped_chunk = (
        CustomStreamWrapper._strip_sse_data_from_chunk(chunk.strip()) or ""
    ).strip()
    if (
        not stripped_chunk
        or stripped_chunk == STREAM_SSE_DONE_STRING
        or stripped_chunk.startswith("event:")
    ):
        return None
    try:
        parsed_chunk = json.loads(stripped_chunk)
    except json.JSONDecodeError:
        return None
    if not isinstance(parsed_chunk, dict):
        return None
    return parsed_chunk

