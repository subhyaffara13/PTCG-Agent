
def _get_model_region(
    custom_llm_provider: str, litellm_params: LiteLLM_Params
) -> Optional[str]:
    """
    Return the region for a model, for a given provider
    """
    if custom_llm_provider == "vertex_ai":
        # check 'vertex_location'
        vertex_ai_location = (
            litellm_params.vertex_location
            or litellm.vertex_location
            or get_secret("VERTEXAI_LOCATION")
            or get_secret("VERTEX_LOCATION")
        )
        if vertex_ai_location is not None and isinstance(vertex_ai_location, str):
            return vertex_ai_location
    elif custom_llm_provider == "bedrock":
        aws_region_name = litellm_params.aws_region_name
        if aws_region_name is not None:
            return aws_region_name
    elif custom_llm_provider == "watsonx":
        watsonx_region_name = litellm_params.watsonx_region_name
        if watsonx_region_name is not None:
            return watsonx_region_name
    return litellm_params.region_name

