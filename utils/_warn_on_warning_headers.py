
def _warn_on_warning_headers(response: httpx.Response) -> None:
    """
    Emit warnings if warning headers are present in the HTTP response.

    Expected header format: 'X-HF-Warning: topic; message'

    Only the first warning for each topic will be shown. Topic is optional and can be empty. Note that several warning
    headers can be present in a single response.

    Args:
        response (`httpx.Response`):
            The HTTP response to check for warning headers.
    """
    server_warnings = response.headers.get_list("X-HF-Warning")
    for server_warning in server_warnings:
        topic, message = server_warning.split(";", 1) if ";" in server_warning else ("", server_warning)
        topic = topic.strip()
        if topic not in _WARNED_TOPICS:
            message = message.strip()
            if message:
                _WARNED_TOPICS.add(topic)
                logger.warning(message)

