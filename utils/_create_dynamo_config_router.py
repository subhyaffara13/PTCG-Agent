
def _create_dynamo_config_router(config_str: str) -> GraphConfigRouter:
    """Create and cache GraphConfigRouter for dynamo config overrides.

    Warns that dynamo config overrides are keyed by frame ID and some configs
    can affect graph breaks, which may shift frame IDs.
    """
    router = GraphConfigRouter(config_str)
    if not router.is_empty():
        warnings.warn(
            "TORCH_COMPILE_OVERRIDE_DYNAMO_CONFIGS is set. Dynamo config overrides are "
            "keyed by frame ID. Some dynamo configs can affect graph breaks, "
            "which may alter the number of frames and shift frame IDs, causing "
            "overrides to target the wrong graphs.",
        )
    return router

