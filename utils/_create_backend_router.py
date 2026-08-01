
def _create_backend_router(config_str: str) -> GraphBackendRouter:
    """Create and cache GraphBackendRouter instances based on config string."""
    return GraphBackendRouter(config_str)

