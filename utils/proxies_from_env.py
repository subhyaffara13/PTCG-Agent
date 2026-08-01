
def proxies_from_env() -> dict[str, ProxyInfo]:
    proxy_urls = {
        k: URL(v)
        for k, v in getproxies().items()
        if k in ("http", "https", "ws", "wss")
    }
    netrc_obj = netrc_from_env()
    stripped = {k: strip_auth_from_url(v) for k, v in proxy_urls.items()}
    ret = {}
    for proto, val in stripped.items():
        proxy, auth = val
        if proxy.scheme in ("https", "wss"):
            client_logger.warning(
                "%s proxies %s are not supported, ignoring", proxy.scheme.upper(), proxy
            )
            continue
        if netrc_obj and auth is None:
            if proxy.host is not None:
                try:
                    auth = basicauth_from_netrc(netrc_obj, proxy.host)
                except LookupError:
                    auth = None
        ret[proto] = ProxyInfo(proxy, auth)
    return ret

