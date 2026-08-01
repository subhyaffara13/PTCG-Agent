
def get_session() -> requests.Session:
    adapter = CacheControlAdapter(
        DictCache(), cache_etags=True, serializer=None, heuristic=None
    )
    sess = requests.Session()
    sess.mount("http://", adapter)
    sess.mount("https://", adapter)

    sess.cache_controller = adapter.controller  # type: ignore[attr-defined]
    return sess


def get_session() -> requests.Session:
    adapter = CacheControlAdapter(
        DictCache(), cache_etags=True, serializer=None, heuristic=None
    )
    sess = requests.Session()
    sess.mount("http://", adapter)
    sess.mount("https://", adapter)

    sess.cache_controller = adapter.controller  # type: ignore[attr-defined]
    return sess


def get_session() -> httpx.Client:
    """
    Get a `httpx.Client` object, using the transport factory from the user.

    This client is shared between all calls made by `huggingface_hub`. Therefore you should not close it manually.

    Use [`set_client_factory`] to customize the `httpx.Client`.
    """
    global _GLOBAL_CLIENT
    if _GLOBAL_CLIENT is None:
        with _CLIENT_LOCK:
            _GLOBAL_CLIENT = _GLOBAL_CLIENT_FACTORY()
    return _GLOBAL_CLIENT

