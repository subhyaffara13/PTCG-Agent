
def _get_llm_provider_headers(response_headers: dict) -> dict:
    """
    Adds a llm_provider-{header} to all headers that are not already prefixed with llm_provider

    Forward all headers as llm_provider-{header}

    """
    llm_provider_headers = {}
    for k, v in response_headers.items():
        if "llm_provider" not in k:
            _key = "{}-{}".format("llm_provider", k)
            llm_provider_headers[_key] = v
        else:
            llm_provider_headers[k] = v
    return llm_provider_headers

