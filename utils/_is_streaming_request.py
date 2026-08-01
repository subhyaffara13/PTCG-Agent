
def _is_streaming_request(
    kwargs: Dict[str, Any],
    call_type: Union[CallTypes, str],
) -> bool:
    """
    Returns True if the call type is a streaming request.
    Returns True if:
        - if "stream=True" in kwargs  (litellm chat completion, litellm text completion, litellm messages)
        - if call_type is generate_content_stream or agenerate_content_stream (litellm google genai)
    """
    if "stream" in kwargs and kwargs["stream"] is True:
        return True
    return call_type in _STREAMING_CALL_TYPES

