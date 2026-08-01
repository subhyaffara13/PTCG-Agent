
def create_proxy_transport_and_mounts():
    proxies = {
        key: None if url is None else Proxy(url=url)
        for key, url in get_environment_proxies().items()
    }

    sync_proxy_mounts = {}
    async_proxy_mounts = {}

    # Retrieve NO_PROXY environment variable
    no_proxy = os.getenv("NO_PROXY", None)
    no_proxy_urls = no_proxy.split(",") if no_proxy else []

    for key, proxy in proxies.items():
        if proxy is None:
            sync_proxy_mounts[key] = httpx.HTTPTransport()
            async_proxy_mounts[key] = httpx.AsyncHTTPTransport()
        else:
            sync_proxy_mounts[key] = httpx.HTTPTransport(proxy=proxy)
            async_proxy_mounts[key] = httpx.AsyncHTTPTransport(proxy=proxy)

    for url in no_proxy_urls:
        sync_proxy_mounts[url] = httpx.HTTPTransport()
        async_proxy_mounts[url] = httpx.AsyncHTTPTransport()

    return sync_proxy_mounts, async_proxy_mounts

