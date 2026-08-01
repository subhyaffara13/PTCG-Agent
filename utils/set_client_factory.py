
def set_client_factory(client_factory: CLIENT_FACTORY_T) -> None:
    """
    Set the HTTP client factory to be used by `huggingface_hub`.

    The client factory is a method that returns a `httpx.Client` object. On the first call to [`get_session`] the client factory
    will be used to create a new `httpx.Client` object that will be shared between all calls made by `huggingface_hub`.

    This can be useful if you are running your scripts in a specific environment requiring custom configuration (e.g. custom proxy or certifications).

    Use [`get_session`] to get a correctly configured `httpx.Client`.
    """
    global _GLOBAL_CLIENT_FACTORY
    with _CLIENT_LOCK:
        close_session()
        _GLOBAL_CLIENT_FACTORY = client_factory

