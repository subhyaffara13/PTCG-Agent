
def _resolve_vertex_model_from_router(
    model_id: str,
    llm_router: Optional[litellm.Router],
    encoded_endpoint: str,
    endpoint: str,
    vertex_project: Optional[str],
    vertex_location: Optional[str],
) -> Tuple[str, str, Optional[str], Optional[str]]:
    """
    Resolve Vertex AI model configuration from router.

    Args:
        model_id: The model ID extracted from the URL (e.g., "gcp/google/gemini-2.5-flash")
        llm_router: The LiteLLM router instance
        encoded_endpoint: The encoded endpoint path
        endpoint: The original endpoint path
        vertex_project: Current vertex project (may be from URL)
        vertex_location: Current vertex location (may be from URL)

    Returns:
        Tuple of (encoded_endpoint, endpoint, vertex_project, vertex_location)
        with resolved values from router config
    """
    if not llm_router:
        return encoded_endpoint, endpoint, vertex_project, vertex_location

    try:
        deployment = llm_router.get_available_deployment_for_pass_through(
            model=model_id
        )
        if not deployment:
            return encoded_endpoint, endpoint, vertex_project, vertex_location

        litellm_params = deployment.get("litellm_params", {})

        # Always override with router config values (they take precedence over URL values)
        config_vertex_project = litellm_params.get("vertex_project")
        config_vertex_location = litellm_params.get("vertex_location")
        if config_vertex_project:
            vertex_project = config_vertex_project
        if config_vertex_location:
            vertex_location = config_vertex_location

        # Get the actual Vertex AI model name by stripping the provider prefix
        # e.g., "vertex_ai/gemini-2.0-flash-exp" -> "gemini-2.0-flash-exp"
        model_from_config = litellm_params.get("model", "")
        if model_from_config:
            # get_llm_provider returns (model, custom_llm_provider, dynamic_api_key, api_base)
            # For "vertex_ai/gemini-2.0-flash-exp" it returns:
            # model="gemini-2.0-flash-exp", custom_llm_provider="vertex_ai"
            actual_model, custom_llm_provider, _, _ = get_llm_provider(
                model=model_from_config
            )

            # Log only non-sensitive information (model names and provider), never API keys or secrets.
            safe_actual_model = actual_model
            safe_custom_llm_provider = custom_llm_provider
            verbose_proxy_logger.debug(
                "get_llm_provider returned: actual_model=%s, custom_llm_provider=%s, model_id=%s",
                safe_actual_model,
                safe_custom_llm_provider,
                model_id,
            )

            if actual_model and model_id != actual_model:
                verbose_proxy_logger.debug(
                    "Resolved router model '%s' to '%s' (provider=%s) with project=%s, location=%s",
                    model_id,
                    actual_model,
                    custom_llm_provider,
                    vertex_project,
                    vertex_location,
                )
                encoded_endpoint = encoded_endpoint.replace(model_id, actual_model)
                endpoint = endpoint.replace(model_id, actual_model)

    except Exception as e:
        verbose_proxy_logger.debug(
            f"Error resolving vertex model from router for model {model_id}: {e}"
        )

    return encoded_endpoint, endpoint, vertex_project, vertex_location

