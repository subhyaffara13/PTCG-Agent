
def _get_valid_models_from_provider_api(
    provider_config: BaseLLMModelInfo,
    custom_llm_provider: str,
    litellm_params: Optional[LiteLLM_Params] = None,
) -> List[str]:
    try:
        cached_result = _model_cache.get_cached_model_info(
            custom_llm_provider, litellm_params
        )

        if cached_result is not None:
            return cached_result
        models = provider_config.get_models(
            api_key=litellm_params.api_key if litellm_params is not None else None,
            api_base=litellm_params.api_base if litellm_params is not None else None,
        )

        _model_cache.set_cached_model_info(custom_llm_provider, litellm_params, models)
        return models
    except Exception as e:
        verbose_logger.warning(f"Error getting valid models: {e}")
        return []

