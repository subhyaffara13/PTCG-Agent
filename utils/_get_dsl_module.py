
def _get_dsl_module(dsl_name: str):
    """Get the registered DSL module for direct control.

    Uses the DSL registry to dynamically look up DSL modules instead of
    hard-coding the mapping. This makes the function automatically extensible
    for new DSLs without code changes.

    Args:
        dsl_name (str): Name of the DSL to retrieve.

    Returns:
        DSLModuleProtocol: The registered DSL module.

    Raises:
        ValueError: If the DSL is not registered.
    """
    registry = _get_dsl_registry()

    # Use the public API to get the DSL module
    dsl_module = registry.get_dsl_module(dsl_name)
    if dsl_module is not None:
        return dsl_module
    else:
        raise ValueError(
            f"Unknown DSL: {dsl_name}. Available DSLs: {registry.list_all_dsls()}"
        )

