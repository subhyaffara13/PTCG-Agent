
def should_use_polling_for_request(
    background_mode: bool,
    polling_via_cache_enabled,  # Can be False, "all", or List[str]
    redis_cache,  # RedisCache or None
    model: str,
    llm_router,  # Router instance or None
    native_background_mode: Optional[
        List[str]
    ] = None,  # List of models that should use native background mode
) -> bool:
    """
    Determine if polling via cache should be used for a request.

    Args:
        background_mode: Whether background=true was set in the request
        polling_via_cache_enabled: Config value - False, "all", or list of providers
        redis_cache: Redis cache instance (required for polling)
        model: Model name from the request (e.g., "gpt-5" or "openai/gpt-4o")
        llm_router: LiteLLM router instance for looking up model deployments
        native_background_mode: List of model names that should use native provider
            background mode instead of polling via cache

    Returns:
        True if polling should be used, False otherwise
    """
    # All conditions must be met
    if not (background_mode and polling_via_cache_enabled and redis_cache):
        return False

    # Check if model is in native_background_mode list - these use native provider background mode
    if native_background_mode and model in native_background_mode:
        verbose_proxy_logger.debug(
            f"Model {model} is in native_background_mode list, skipping polling via cache"
        )
        return False

    # "all" enables polling for all providers
    if polling_via_cache_enabled == "all":
        return True

    # Check if provider is in the enabled list
    if isinstance(polling_via_cache_enabled, list):
        # First, try to get provider from model string format "provider/model"
        if "/" in model:
            provider = model.split("/")[0]
            if provider in polling_via_cache_enabled:
                return True
        # Otherwise, check ALL deployments for this model_name in router
        elif llm_router is not None:
            try:
                # Get all deployment indices for this model name
                indices = llm_router.model_name_to_deployment_indices.get(model, [])
                for idx in indices:
                    deployment_dict = llm_router.model_list[idx]
                    litellm_params = deployment_dict.get("litellm_params", {})

                    # Check custom_llm_provider first
                    dep_provider = litellm_params.get("custom_llm_provider")

                    # Then try to extract from model (e.g., "openai/gpt-5")
                    if not dep_provider:
                        dep_model = litellm_params.get("model", "")
                        if "/" in dep_model:
                            dep_provider = dep_model.split("/")[0]

                    # If ANY deployment's provider matches, enable polling
                    if dep_provider and dep_provider in polling_via_cache_enabled:
                        verbose_proxy_logger.debug(
                            f"Polling enabled for model={model}, provider={dep_provider}"
                        )
                        return True
            except Exception as e:
                verbose_proxy_logger.debug(
                    f"Could not resolve provider for model {model}: {e}"
                )

    return False

