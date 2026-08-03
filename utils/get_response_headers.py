from typing import Optional

def get_response_headers(_response_headers: Optional[dict] = None) -> dict:
    """

    Sets the Appropriate OpenAI headers for the response and forward all headers as llm_provider-{header}

    Note: _response_headers Passed here should be OpenAI compatible headers

    Args:
        _response_headers (Optional[dict], optional): _response_headers. Defaults to None.

    Returns:
        dict: _response_headers with OpenAI headers and llm_provider-{header}

    """
    if _response_headers is None:
        return {}

    openai_headers = {}
    if "x-ratelimit-limit-requests" in _response_headers:
        openai_headers["x-ratelimit-limit-requests"] = _response_headers[
            "x-ratelimit-limit-requests"
        ]
    if "x-ratelimit-remaining-requests" in _response_headers:
        openai_headers["x-ratelimit-remaining-requests"] = _response_headers[
            "x-ratelimit-remaining-requests"
        ]
    if "x-ratelimit-limit-tokens" in _response_headers:
        openai_headers["x-ratelimit-limit-tokens"] = _response_headers[
            "x-ratelimit-limit-tokens"
        ]
    if "x-ratelimit-remaining-tokens" in _response_headers:
        openai_headers["x-ratelimit-remaining-tokens"] = _response_headers[
            "x-ratelimit-remaining-tokens"
        ]
    llm_provider_headers = _get_llm_provider_headers(_response_headers)
    return {**llm_provider_headers, **openai_headers}

