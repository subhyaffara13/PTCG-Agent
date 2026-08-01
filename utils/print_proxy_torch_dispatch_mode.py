
def print_proxy_torch_dispatch_mode(
    mode: ProxyTorchDispatchMode, format_str: str, *args: object, **kwargs: object
) -> None:
    proxy_args = pytree.tree_map(mode.tracer.unwrap_proxy, args)  # type: ignore[union-attr]
    proxy_kwargs = pytree.tree_map(mode.tracer.unwrap_proxy, kwargs)  # type: ignore[union-attr]
    mode.tracer.create_proxy(
        "call_function", print, (format_str, *proxy_args), proxy_kwargs
    )

