from typing import Optional, Tuple

def rerank_cost(
    model: str,
    custom_llm_provider: Optional[str],
    billed_units: Optional[RerankBilledUnits] = None,
) -> Tuple[float, float]:
    """
    Returns
    - float or None: cost of response OR none if error.
    """
    _, custom_llm_provider, _, _ = litellm.get_llm_provider(
        model=model, custom_llm_provider=custom_llm_provider
    )

    try:
        config = ProviderConfigManager.get_provider_rerank_config(
            model=model,
            api_base=None,
            present_version_params=[],
            provider=LlmProviders(custom_llm_provider),
        )

        try:
            model_info: Optional[ModelInfo] = litellm.get_model_info(
                model=model, custom_llm_provider=custom_llm_provider
            )
        except Exception:
            model_info = None

        return config.calculate_rerank_cost(
            model=model,
            custom_llm_provider=custom_llm_provider,
            billed_units=billed_units,
            model_info=model_info,
        )
    except Exception as e:
        raise e

