
def get_async_session() -> httpx.AsyncClient:
    """
    Return a `httpx.AsyncClient` object, using the transport factory from the user.

    Use [`set_async_client_factory`] to customize the `httpx.AsyncClient`.

    <Tip warning={true}>

    Contrary to the `httpx.Client` that is shared between all calls made by `huggingface_hub`, the `httpx.AsyncClient` is not shared.
    It is recommended to use an async context manager to ensure the client is properly closed when the context is exited.

    </Tip>
    """
    return _GLOBAL_ASYNC_CLIENT_FACTORY()

