
def run_const_graph_dispatch_mode(
    mode: ProxyTorchDispatchMode, graph: torch.fx.GraphModule, args: tuple[object, ...]
) -> object:
    const_gm, weights = graph, args
    p_args = pytree.tree_map(mode.tracer.unwrap_proxy, (graph, args))  # type: ignore[union-attr]
    if not isinstance(const_gm, torch.fx.GraphModule):
        raise AssertionError(
            f"expected const_gm to be torch.fx.GraphModule, got {type(const_gm)}"
        )
    if hasattr(mode.tracer.root, "_const_graph"):  # type: ignore[union-attr]
        raise AssertionError("mode.tracer.root already has _const_graph attribute")
    mode.tracer.root.register_module("_const_graph", const_gm)  # type: ignore[union-attr]

    proxy = mode.tracer.create_proxy("call_function", run_const_graph, p_args, {})

    out = const_gm(*weights)
    return track_tensor_tree(out, proxy, constant=None, tracer=mode.tracer)

