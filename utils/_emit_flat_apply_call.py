
def _emit_flat_apply_call(
    *,
    tracer,
    spec_name: str,
    const_target_for_apply,
    graphable_args,
    track_value,
    call_spec_cache_key: str,
):
    # Flatten to graphable form and record the spec on the FX root
    flat_args, in_spec = to_graphable(graphable_args)
    qualname = tracer.get_fresh_qualname(spec_name)  # type: ignore[union-attr]
    setattr(tracer.root, qualname, in_spec)  # type: ignore[union-attr]
    spec_proxy = tracer.create_proxy("get_attr", qualname, (), {})

    # Reuse/cached ConstantFunction spec on the root
    _, func_spec = pytree.tree_flatten(_ConstantFunction(const_target_for_apply))
    func_spec_proxy = _register_func_spec_proxy_in_tracer(
        tracer, f"{call_spec_cache_key}_const_func_spec", func_spec
    )

    # Map runtime args -> proxies (always via tracer.unwrap_proxy now)
    flat_proxy_args = pytree.tree_map(tracer.unwrap_proxy, flat_args)

    # Emit flat_apply and track result structure
    out_proxy = tracer.create_proxy(
        "call_function", flat_apply, (func_spec_proxy, spec_proxy, *flat_proxy_args), {}
    )
    track_tensor_tree(track_value, out_proxy, constant=None, tracer=tracer)

