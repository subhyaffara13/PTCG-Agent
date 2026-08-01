
def add_retry_headers_to_response(
    response: Any,
    attempted_retries: int,
    max_retries: Optional[int] = None,
) -> Any:
    """
    Add retry headers to the request
    """
    retry_headers = {
        "x-litellm-attempted-retries": attempted_retries,
    }
    if max_retries is not None:
        retry_headers["x-litellm-max-retries"] = max_retries

    return _add_headers_to_response(response, retry_headers)

