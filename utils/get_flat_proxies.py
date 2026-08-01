
def get_flat_proxies(fingerprint: InputFingerprint) -> list[Proxy]:
    """Collect deduplicated proxies from tensor/symnode leaves."""
    seen: set[torch.fx.Node] = set()
    flat_proxies: list[Proxy] = []
    for tag, vt in fingerprint.flat_vts:
        if tag in (InputTag.TENSOR, InputTag.SYMNODE):
            proxy = vt.as_proxy()
            if proxy.node not in seen:
                seen.add(proxy.node)
                flat_proxies.append(proxy)
    return flat_proxies

