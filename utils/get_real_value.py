
def get_real_value(node: torch.fx.Node, tracer: Any) -> Any:
    """
    Run the actual computation represented by `node` and return the result.
    This will execute any dependent nodes in the graph as well.
    """
    from . import graph_break_hints
    from .exc import unimplemented

    cache = tracer.real_value_cache
    if node in cache:
        return cache[node]

    op = node.op
    args, kwargs = torch.fx.node.map_arg(  # type: ignore[misc]
        (node.args, node.kwargs),
        lambda n: get_real_value(n, tracer),
    )

    if op == "placeholder" and "grapharg" in node.meta:
        return node.meta["grapharg"].example

    if op == "call_module":
        nn_module = tracer.output_graph.nn_modules[node.target]
        if not is_lazy_module(nn_module):
            nn_module = copy.deepcopy(nn_module)
        else:
            # In the case of a lazy module, we want to run
            # the pre-hooks which initialize it
            nn_module(*args, **kwargs)
    else:
        nn_module = None

    try:
        real_value = run_node(tracer, node, args, kwargs, nn_module)
        cache[node] = real_value
    except RuntimeError as e:
        exn = e  # to make typing happy for the lambda
        _wrap_graph_break_with_torch_runtime_err(
            lambda: unimplemented(
                gb_type="RuntimeError when trying to get real value from fx.Node",
                context="",
                explanation="",
                hints=[*graph_break_hints.USER_ERROR],
                from_exc=exn,
            )
        )
        raise AssertionError("should not be reachable") from None
    return real_value

