
def _register_all_overrides() -> None:
    """
    Perform all registration calls from previously-built override graphs.
    """
    for key, graph in _graphs.items():
        op_symbol, dispatch_key = key

        _register_overrides_from_graph(
            op_symbol,
            dispatch_key,
            graph,
        )

