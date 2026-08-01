
def _is_streaming_response(response: httpx.Response) -> bool:
    _content_type = response.headers.get("content-type")
    if _content_type is not None and "text/event-stream" in _content_type:
        return True
    return False

