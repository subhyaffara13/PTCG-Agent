
def _prepare_registry_credentials(
    *,
    vector_store_id: str,
    kwargs: Dict[str, Any],
) -> None:
    if litellm.vector_store_registry is None:
        return
    try:
        registry_credentials = (
            litellm.vector_store_registry.get_credentials_for_vector_store(
                vector_store_id
            )
        )
        if registry_credentials:
            kwargs.update(registry_credentials)
    except Exception:
        pass

