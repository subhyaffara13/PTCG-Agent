
def request_log(
    logger: logging.Logger,
    method: str,
    url: str,
    body: Optional[bytes],
    headers: Optional[Mapping[str, str]],
) -> None:
    """
    Logs an HTTP request at the DEBUG level if logging is enabled.

    Args:
        logger: The logging.Logger instance to use.
        method: The HTTP method (e.g., "GET", "POST").
        url: The URL of the request.
        body: The request body (can be None).
        headers: The request headers (can be None).
    """
    if is_logging_enabled(logger):
        content_type = (
            headers["Content-Type"] if headers and "Content-Type" in headers else ""
        )
        json_body = _parse_request_body(body, content_type=content_type)
        logged_body = _hash_sensitive_info(json_body)
        logger.debug(
            "Making request...",
            extra={
                "httpRequest": {
                    "method": method,
                    "url": url,
                    "body": logged_body,
                    "headers": headers,
                }
            },
        )

