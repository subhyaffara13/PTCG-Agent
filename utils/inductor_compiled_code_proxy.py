
def inductor_compiled_code_proxy(mode, func, inputs, *, name=None):
    resolved = _resolve_inductor_callable(func)

    # Run the fake impl to get example outputs for tracing
    kwargs = {"name": name} if name is not None else {}
    example_out = inductor_compiled_code(func, inputs, **kwargs)

    # Register in side table so the FX node stores a serializable int
    callable_idx = inductor_code_side_table.add_callable(resolved)

    proxy_inputs = pytree.tree_map(mode.tracer.unwrap_proxy, inputs)

    out_proxy = mode.tracer.create_proxy(
        "call_function",
        inductor_compiled_code,
        (callable_idx, proxy_inputs),
        kwargs,
    )

    return track_tensor_tree(example_out, out_proxy, constant=None, tracer=mode.tracer)

