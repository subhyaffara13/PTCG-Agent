
def raise_text_generation_error(http_error: HfHubHTTPError) -> NoReturn:
    """
    Try to parse text-generation-inference error message and raise HTTPError in any case.

    Args:
        error (`HTTPError`):
            The HTTPError that have been raised.
    """
    # Try to parse a Text Generation Inference error
    if http_error.response is None:
        raise http_error

    try:
        # Hacky way to retrieve payload in case of aiohttp error
        payload = getattr(http_error, "response_error_payload", None) or http_error.response.json()
        error = payload.get("error")
        error_type = payload.get("error_type")
    except Exception:  # no payload
        raise http_error

    # If error_type => more information than `hf_raise_for_status`
    if error_type is not None:
        exception = _parse_text_generation_error(error, error_type)
        raise exception from http_error

    # Otherwise, fallback to default error
    raise http_error

