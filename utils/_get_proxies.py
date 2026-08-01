
def _get_proxies(t: torch.Tensor) -> list[Proxy]:
    proxies = []
    mode = torch._C._get_dispatch_mode(torch._C._TorchDispatchModeKey.PROXY)
    if mode is None:
        return proxies
    if not isinstance(mode, ProxyTorchDispatchMode):
        raise AssertionError(f"Expected ProxyTorchDispatchMode, got {type(mode)}")
    tracer = mode.tracer
    for t_inner in get_plain_tensors(t, out=[]):
        if isinstance(t_inner, FunctionalTensor):
            t_inner = torch._from_functional_tensor(t_inner.elem)
        if not isinstance(t_inner, torch.Tensor):
            continue
        proxy_tensor = get_proxy_slot(t_inner, tracer)
        if proxy_tensor is not None:
            proxies.append(proxy_tensor.proxy)
    return proxies

