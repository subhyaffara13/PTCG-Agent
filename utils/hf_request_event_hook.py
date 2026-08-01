
def hf_request_event_hook(request: httpx.Request) -> None:
    """
    Event hook that will be used to make HTTP requests to the Hugging Face Hub.

    What it does:
    - Block requests if offline mode is enabled
    - Add a request ID to the request headers
    - Log the request if debug mode is enabled
    """
    if constants.is_offline_mode():
        raise OfflineModeIsEnabled(
            f"Cannot reach {request.url}: offline mode is enabled. To disable it, please unset the `HF_HUB_OFFLINE` environment variable."
        )

    # Add random request ID => easier for server-side debugging
    if X_AMZN_TRACE_ID not in request.headers:
        request.headers[X_AMZN_TRACE_ID] = request.headers.get(X_REQUEST_ID) or str(uuid.uuid4())
    request_id = request.headers.get(X_AMZN_TRACE_ID)

    # Debug log
    logger.debug(
        "Request %s: %s %s (authenticated: %s)",
        request_id,
        request.method,
        request.url,
        request.headers.get("authorization") is not None,
    )
    if constants.HF_DEBUG:
        logger.debug("Send: %s", _curlify(request))

    return request_id

