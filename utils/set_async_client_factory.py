
def set_async_client_factory(async_client_factory: ASYNC_CLIENT_FACTORY_T) -> None:
    """
    Set the HTTP async client factory to be used by `huggingface_hub`.

    The async client factory is a method that returns a `httpx.AsyncClient` object.
    This can be useful if you are running your scripts in a specific environment requiring custom configuration (e.g. custom proxy or certifications).
    Use [`get_async_client`] to get a correctly configured `httpx.AsyncClient`.

    <Tip warning={true}>

    Contrary to the `httpx.Client` that is shared between all calls made by `huggingface_hub`, the `httpx.AsyncClient` is not shared.
    It is recommended to use an async context manager to ensure the client is properly closed when the context is exited.

    </Tip>
    """
    global _GLOBAL_ASYNC_CLIENT_FACTORY
    _GLOBAL_ASYNC_CLIENT_FACTORY = async_client_factory

