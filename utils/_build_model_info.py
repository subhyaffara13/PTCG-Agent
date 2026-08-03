from typing import Optional

def _build_model_info(
    model: str,
    custom_llm_provider: Optional[str] = None,
    api_base: Optional[str] = None,
    api_key: Optional[str] = None,
) -> ModelInfo:
    supported_openai_params = litellm.get_supported_openai_params(
        model=model, custom_llm_provider=custom_llm_provider
    )

    _model_info = _get_model_info_helper(
        model=model,
        custom_llm_provider=custom_llm_provider,
        api_base=api_base,
        api_key=api_key,
    )

    provider_info = get_provider_info(
        model=model, custom_llm_provider=custom_llm_provider
    )
    if provider_info:
        for key, value in provider_info.items():
            if value is not None:
                _model_info[key] = value  # type: ignore

    # if verbose_logger.isEnabledFor(logging.DEBUG):
    # verbose_logger.debug(f"model_info: {_model_info}")

    return ModelInfo(**_model_info, supported_openai_params=supported_openai_params)

