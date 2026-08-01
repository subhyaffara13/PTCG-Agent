
def _decompose_scatter_mutating(
    graph: torch.fx.Graph, node: torch.fx.Node
) -> torch.fx.Node:
    """Decompose _generalized_scatter using mutations

    e.g. _generalized_scatter(inp, src, [(aten.slice, 0, 0, 10), (aten.slice, 1, 10, -10)])

    will become

    inp_updated = aten.clone(inp)
    slice1 = aten.slice(inp_updated, 0, 0, 10)
    slice2 = aten.slice(slice1, 1, 10, -10)
    slice2.copy_(src)

    """
    assert node.target in (_generalized_scatter, _inplace_generalized_scatter)
    inp, src, view_ops = node.args
    assert not node.kwargs

    if node.target is _generalized_scatter:
        inp = graph_call_function(graph, aten.clone, inp)

    tmp = inp
    for view in view_ops:  # type: ignore[union-attr]
        tmp = graph_call_function(graph, view.target, tmp, *view.args, **view.kwargs)  # type: ignore[union-attr]
        # we need to set unbacked bindings that could have been created in the view ops.
        if (V.fake_mode.shape_env) and (
            symbol_to_path := compute_unbacked_bindings(
                V.fake_mode.shape_env, tmp.meta["val"]
            )
        ):
            tmp.meta["unbacked_bindings"] = symbol_to_path

    graph_call_function(graph, aten.copy_.default, tmp, src)
    return inp  # type: ignore[return-value]

