
def disable_proxy_modes_tracing() -> Generator[ProxyTorchDispatchMode, None, None]:
    return _disable_infra_mode(torch._C._TorchDispatchModeKey.PROXY)

