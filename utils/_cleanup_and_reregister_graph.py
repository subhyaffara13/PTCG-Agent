
def _cleanup_and_reregister_graph(
    op_symbol: str,
    dispatch_key: str,
    graph: list[_OverrideNode],
    *,
    filter_state: _FilterState | None = None,
) -> None:
    """
    Clean up existing library and reregister a graph.

    This is the common pattern used across reorder, deregister, and reenable operations.

    Args:
        op_symbol: The operation symbol
        dispatch_key: The dispatch key
        graph: The graph to register
        filter_state: Optional filter state for conditional registration
    """
    key = (op_symbol, dispatch_key)

    # Remove existing library if it exists
    if key in _libs:
        del _libs[key]

    # Only create a library if the graph has nodes
    # Empty graphs (disabled operations) shouldn't get libraries
    if graph:
        _register_overrides_from_graph(
            op_symbol,
            dispatch_key,
            graph,
            filter_state=filter_state,
        )

