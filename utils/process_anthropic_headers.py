
def process_anthropic_headers(headers: Union[httpx.Headers, dict]) -> dict:
    openai_headers = {}
    if "anthropic-ratelimit-requests-limit" in headers:
        openai_headers["x-ratelimit-limit-requests"] = headers[
            "anthropic-ratelimit-requests-limit"
        ]
    if "anthropic-ratelimit-requests-remaining" in headers:
        openai_headers["x-ratelimit-remaining-requests"] = headers[
            "anthropic-ratelimit-requests-remaining"
        ]
    if "anthropic-ratelimit-tokens-limit" in headers:
        openai_headers["x-ratelimit-limit-tokens"] = headers[
            "anthropic-ratelimit-tokens-limit"
        ]
    if "anthropic-ratelimit-tokens-remaining" in headers:
        openai_headers["x-ratelimit-remaining-tokens"] = headers[
            "anthropic-ratelimit-tokens-remaining"
        ]

    llm_response_headers = {
        "{}-{}".format("llm_provider", k): v for k, v in headers.items()
    }

    additional_headers = {**llm_response_headers, **openai_headers}
    return additional_headers

