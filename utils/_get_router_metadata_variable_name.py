
def _get_router_metadata_variable_name(function_name: Optional[str]) -> str:
    """
    Helper to return what the "metadata" field should be called in the request data

    For all /thread or /assistant endpoints we need to call this "litellm_metadata"

    For ALL other endpoints we call this "metadata
    """
    ROUTER_METHODS_USING_LITELLM_METADATA = set(
        [
            "batch",
            "generic_api_call",
            "_acreate_batch",
            "file",
            "_ageneric_api_call_with_fallbacks",
        ]
    )
    if function_name and any(
        method in function_name for method in ROUTER_METHODS_USING_LITELLM_METADATA
    ):
        return "litellm_metadata"
    else:
        return "metadata"

