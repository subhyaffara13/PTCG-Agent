
def _create_inductor_config_router(config_str: str) -> GraphConfigRouter:
    """Create and cache GraphConfigRouter for inductor config overrides."""
    return GraphConfigRouter(config_str)

