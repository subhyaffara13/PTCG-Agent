
def flatten_graph_inputs(
    gm: torch.fx.GraphModule, inputs: Any, compile_gm: Callable[[Any, Any], Any]
) -> Callable[..., Any]:
    """
    Mutate inputs so that they are flat and wrap gm such that it
    accepts those inputs.  This is needed for graphs that take
    bumpy inputs.
    """
    inputs_idx_to_clear = [
        i
        for i, node in enumerate(gm.graph.nodes)
        if node.op == "placeholder" and node.meta.get("steal_arg", False)
    ]

    if torch._dynamo.compiled_autograd.in_compiled_autograd_region:
        # fast path, avoid pytree overhead
        # compiled autograd inputs are always a list of tensors, maybe followed by symints
        assert inputs_idx_to_clear == [0]
        assert isinstance(inputs[0], list)
        boxed_inputs_count = len(inputs[0])

        def flatten_fn(args: Any) -> Any:
            return args[0] + list(args[1:])

        def unflatten_fn(flat_args: Any) -> Any:
            return (flat_args[:boxed_inputs_count], *flat_args[boxed_inputs_count:])

        compiled_fn = compile_gm(GmWrapper(gm, unflatten_fn), flatten_fn(inputs))
    else:
        # slow path, don't know inputs structure
        flat_inputs, spec = pytree.tree_flatten(inputs)
        unflatten_fn = functools.partial(pytree.tree_unflatten, treespec=spec)
        compiled_fn = compile_gm(GmWrapper(gm, unflatten_fn), flat_inputs)
        # note this doesn't check the spec, assuming it is the same
        flatten_fn = pytree.arg_tree_leaves

    def wrapper(*args: Any) -> Any:
        flat_args = flatten_fn(args)

        # flat_args is a new list, so we need to clear references from the old list
        for i in inputs_idx_to_clear:
            args[i].clear()

        # this call is boxed to avoid increasing refcount until we reach aot_module_simplified forward
        return compiled_fn(flat_args)

    return wrapper

