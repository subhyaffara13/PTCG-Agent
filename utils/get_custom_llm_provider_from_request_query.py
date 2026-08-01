
def get_custom_llm_provider_from_request_query(request: Request) -> Optional[str]:
    """
    Get the `custom_llm_provider` from the request query parameters

    Safely reads the request query parameters
    """
    if "custom_llm_provider" in request.query_params:
        return request.query_params["custom_llm_provider"]
    return None

