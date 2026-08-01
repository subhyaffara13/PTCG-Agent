
def get_ingestion_class(provider: str) -> Type[BaseRAGIngestion]:
    """
    Get the ingestion class for a given provider.

    Args:
        provider: The vector store provider name (e.g., 'openai')

    Returns:
        The ingestion class for the provider

    Raises:
        ValueError: If provider is not supported
    """
    ingestion_class = INGESTION_REGISTRY.get(provider)
    if ingestion_class is None:
        supported = ", ".join(INGESTION_REGISTRY.keys())
        raise ValueError(
            f"Provider '{provider}' is not supported for RAG ingestion. "
            f"Supported providers: {supported}"
        )
    return ingestion_class

