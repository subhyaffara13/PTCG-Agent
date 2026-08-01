
def proxy_mode_key(
    proxy_mode: ProxyTorchDispatchMode,
    gm: GraphModule,
    *args: Any,
    **kwargs: Any,
) -> tuple[torch.Tensor]:
    # TODO: get rid of this when we can install as a subgraph
    def call_local_map(*_args: Any, **_kwargs: Any) -> Any:
        return functools.partial(local_map_hop, gm)(*_args, **_kwargs)

    return proxy_mode_key_common(call_local_map, proxy_mode, gm, *args, **kwargs)


def proxy_mode_key(
    proxy_mode: ProxyTorchDispatchMode,
    gmod: GraphModule,
    *args: Any,
    **kwargs: Any,
) -> tuple[torch.Tensor]:
    import torch.fx.traceback as fx_traceback
    from torch.fx import Interpreter

    if not proxy_mode.pre_dispatch:
        raise AssertionError(
            "post-dispatch mode should have inlined in the Autograd key"
        )
    example_out = tag_activation_checkpoint(gmod, *args, **kwargs)
    proxy_args = pytree.tree_map(proxy_mode.tracer.unwrap_proxy, args)  # type: ignore[union-attr]
    proxy_kwargs = pytree.tree_map(proxy_mode.tracer.unwrap_proxy, kwargs)  # type: ignore[union-attr]
    qualname = proxy_mode.tracer.get_fresh_qualname("wrap_body")  # type: ignore[union-attr]

    # TODO (tmanlaibaatar) don't we need flat_apply here??
    # Dynamo already traced the gmod body without kwargs
    flat_args, _ = pytree.tree_flatten(args)
    with fx_traceback.preserve_node_meta():
        gmod_aten = reenter_make_fx(Interpreter(gmod).run)(*flat_args)
        gmod_aten.meta["_checkpoint_context_fn"] = gmod.meta["_checkpoint_context_fn"]
    proxy_mode.tracer.root.register_module(qualname, gmod_aten)  # type: ignore[union-attr]
    proxy_gmod = proxy_mode.tracer.unwrap_proxy(gmod_aten)  # type: ignore[union-attr, call-overload]
    out_proxy = proxy_mode.tracer.create_proxy(
        "call_function",
        tag_activation_checkpoint,
        (proxy_gmod, *proxy_args),
        proxy_kwargs,
    )
    return track_tensor_tree(
        example_out, out_proxy, constant=None, tracer=proxy_mode.tracer
    )

