
def vector_store_search_cost(
    model: Optional[str],
    custom_llm_provider: str,
    response: VectorStoreSearchResponse,
) -> Tuple[float, float]:
    """
    Returns
    - float or None: cost of vector store search
    """
    api_type: Optional[str] = None
    if custom_llm_provider is None:
        custom_llm_provider = "openai"

    if model is not None and "/" in model:
        api_type, custom_llm_provider, _, _ = litellm.get_llm_provider(
            model=model,
        )

    config = ProviderConfigManager.get_provider_vector_stores_config(
        provider=LlmProviders(custom_llm_provider),
        api_type=api_type,
    )

    if config is None:
        verbose_logger.debug(
            f"Vector store search is not supported for {custom_llm_provider}"
        )
        return 0.0, 0.0

    return config.calculate_vector_store_cost(
        response=response,
    )

