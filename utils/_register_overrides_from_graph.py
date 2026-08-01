
def _register_overrides_from_graph(
    op_symbol: str,
    dispatch_key: str,
    graph: list[_OverrideNode],
    *,
    filter_state: _FilterState | None = None,
) -> None:
    """
    Register all overrides in a single graph.

    Args:
        op_symbol: The operation symbol
        dispatch_key: The dispatch key
        graph: List of override nodes to register
        filter_state: Optional filter state for conditional registration
    """
    key = (op_symbol, dispatch_key)
    lib = _get_or_create_library(*key)

    for node in graph:
        enable = True
        if filter_state:
            enable = filter_state.check_enabled(node)

        if enable:
            _register_node_impl(lib, node, dispatch_key)
            node.active = True
        else:
            node.active = False

