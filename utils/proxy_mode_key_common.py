
def proxy_mode_key_common(
    call_hop: Callable[..., Any],
    proxy_mode: ProxyTorchDispatchMode,
    gm: GraphModule,
    *args: Any,
    **kwargs: Any,
) -> tuple[torch.Tensor]:
    if proxy_mode is None:
        raise AssertionError("Mode should always be enabled for python fallback key")
    if len(kwargs) != 0:
        raise AssertionError(f"kwargs must be empty, got {kwargs}")

    example_out = call_hop(*args, **kwargs)
    proxy_args = pytree.tree_map(proxy_mode.tracer.unwrap_proxy, args)  # type: ignore[union-attr]

    out_proxy = proxy_mode.tracer.create_proxy(
        "call_function", call_hop, proxy_args, {}
    )

    # extract local_map args, post-dispatch operates on GraphModules
    if not gm.meta["local_map_kwargs"]:
        raise AssertionError("gm.meta['local_map_kwargs'] must be set")
    local_map_kwargs = gm.meta["local_map_kwargs"]

    # propagate local_map args to the call_function node
    out_proxy.node.meta["local_map_kwargs"] = local_map_kwargs

    return track_tensor_tree(
        example_out, out_proxy, constant=None, tracer=proxy_mode.tracer
    )

