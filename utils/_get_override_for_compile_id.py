
def _get_override_for_compile_id(
    compile_id: CompileId | None,
    config_str: str,
    create_router: Callable[[str], _GraphRouterBase[T]],
    label: str,
) -> T | None:
    """
    Get the override value for a given CompileId.

    Returns the value from the router, or None if no override applies.
    """
    if compile_id is None or not config_str:
        return None

    graph_id = compile_id.frame_id
    if graph_id is None:
        return None

    router = create_router(config_str)
    value = router.get_value_for_graph(graph_id)
    if value is not None:
        log.info("Overriding %s: %s", label, value)
    return value

