
def get_custom_llm_provider_from_request_headers(request: Request) -> Optional[str]:
    """
    Get the `custom_llm_provider` from the request header `custom-llm-provider`
    """
    if "custom-llm-provider" in request.headers:
        return request.headers["custom-llm-provider"]
    return None

