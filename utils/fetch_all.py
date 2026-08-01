
def fetch_all(
    endpoint: str, args: str = "", *, timeout: float
) -> tuple[list[str], list[Response]]:
    store = tcpstore_client()
    keys = [f"rank{r}" for r in range(get_world_size())]
    addrs = store.multi_get(keys)
    addrs = [f"{addr.decode()}/handler/{endpoint}?{args}" for addr in addrs]

    try:
        resps = fetch_aiohttp(addrs, timeout=timeout)
    except ImportError:
        resps = fetch_thread_pool(addrs, timeout=timeout)

    return addrs, resps

