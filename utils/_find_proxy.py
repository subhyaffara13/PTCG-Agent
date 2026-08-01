
def _find_proxy(*objects_to_search: object) -> Proxy | None:
    """
    Recursively search a data structure for a Proxy() and return it,
    return None if not found.
    """
    proxy = None

    def find_proxy(x: object) -> None:
        nonlocal proxy
        if isinstance(x, Proxy):
            proxy = x

    # pyrefly: ignore[bad-specialization]
    map_aggregate(objects_to_search, find_proxy)
    return proxy

