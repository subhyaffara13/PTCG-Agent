
def trace_strict_mode(mode, strict_mode_op, callable, operands):
    pre_dispatch = getattr(mode, "pre_dispatch", False)

    with disable_proxy_modes_tracing():
        graph = make_fx(callable, pre_dispatch=pre_dispatch)(*operands)

    graph_name = mode.tracer.get_fresh_qualname("strict_graph_")
    mode.tracer.root.register_module(graph_name, graph)

    args = (graph, operands)

    proxy_args = pytree.tree_map(mode.tracer.unwrap_proxy, args)

    out_proxy = mode.tracer.create_proxy(
        "call_function", strict_mode_op, proxy_args, {}, name="strict_mode"
    )

    out = graph(*operands)
    return track_tensor_tree(out, out_proxy, constant=None, tracer=mode.tracer)

