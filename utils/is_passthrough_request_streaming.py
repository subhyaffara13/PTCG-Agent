
def is_passthrough_request_streaming(request_body: dict) -> bool:
    """
    Returns True if the request is streaming
    """
    return request_body.get("stream", False)

