from typing import Any

def inner_trace(
    mode: ProxyTorchDispatchMode,
    *args: Any,
    bw_state: BackwardState | None = None,
    **kwargs: Any,
) -> Any:
    def self_invoke(*args: Any, **dyn_kwargs: Any) -> Any:
        with torch.no_grad():
            return _trace_wrapped_op(*args, **dyn_kwargs, **kwargs)

    def unwrap_proxies(x: Any) -> Any:
        if isinstance(x, torch.Tensor):
            return mode.tracer.unwrap_proxy(x)  # type: ignore[union-attr]
        if isinstance(x, (list, tuple)):
            return type(x)(map(unwrap_proxies, x))
        if x is None:
            return None
        raise AssertionError(f"unhandled type: {type(x)}")

    proxy_kwargs = {}
    if bw_state is not None:
        assert isinstance(bw_state, BackwardState) and bw_state.proxy is not None
        proxy_kwargs["bw_state"] = bw_state.proxy
    out_proxy = mode.tracer.create_proxy(
        "call_function",
        self_invoke,
        unwrap_proxies(args),
        proxy_kwargs,
        name="trace_wrapped",
    )

    if args[0] is None:
        grad = args[1]  # module backward hooks
    else:
        grad = args[0]  # other backward hooks
    grad = tree_map_only(torch.Tensor, torch.empty_like, grad)
    track_tensor_tree(grad, out_proxy, constant=None, tracer=mode.tracer)
    return grad

