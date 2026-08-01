
def _override_vertex_params_from_router_credentials(
    router_credentials: Optional[Any],
    vertex_project: Optional[str],
    vertex_location: Optional[str],
) -> Tuple[Optional[str], Optional[str]]:
    """
    Override vertex_project and vertex_location with values from router_credentials if available.

    Args:
        router_credentials: Optional vector store credentials from registry (LiteLLM_ManagedVectorStore)
        vertex_project: Current vertex project ID (from URL)
        vertex_location: Current vertex location (from URL)

    Returns:
        Tuple of (vertex_project, vertex_location) with overridden values if applicable
    """
    if router_credentials is None:
        return vertex_project, vertex_location

    verbose_proxy_logger.debug(
        "Using vector store credentials to override vertex project and location"
    )

    litellm_params = router_credentials.get("litellm_params", {})
    if not litellm_params:
        verbose_proxy_logger.warning(
            "Vector store credentials found but litellm_params is empty"
        )
        return vertex_project, vertex_location

    # Extract vertex_project and vertex_location from litellm_params
    vector_store_project = litellm_params.get("vertex_project")
    vector_store_location = litellm_params.get("vertex_location")

    if vector_store_project:
        verbose_proxy_logger.debug(
            "Overriding vertex_project from URL (%s) with vector store value: %s",
            vertex_project,
            vector_store_project,
        )
        vertex_project = vector_store_project
    else:
        verbose_proxy_logger.warning(
            "Vector store credentials found but missing vertex_project in litellm_params"
        )

    if vector_store_location:
        verbose_proxy_logger.debug(
            "Overriding vertex_location from URL (%s) with vector store value: %s",
            vertex_location,
            vector_store_location,
        )
        vertex_location = vector_store_location
    else:
        verbose_proxy_logger.warning(
            "Vector store credentials found but missing vertex_location in litellm_params"
        )

    return vertex_project, vertex_location

