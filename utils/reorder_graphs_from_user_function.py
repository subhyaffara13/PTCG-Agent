
def reorder_graphs_from_user_function(
    fn: UserOrderingFn,
    *,
    reregister_overrides: bool = False,
) -> None:
    """
    Reorder override graphs using a user-provided ordering function.

    Args:
        fn: User-provided function that takes (op_symbol, dispatch_key, graph)
            and returns a reordered graph
        reregister_overrides: Whether to reregister graphs that have changed

    Note:
        This function uses the common graph transformation pattern and can serve
        as an example for other graph manipulation operations.
    """
    _apply_graph_transformation(
        transformation_fn=fn,
        reregister_overrides=reregister_overrides,
    )

