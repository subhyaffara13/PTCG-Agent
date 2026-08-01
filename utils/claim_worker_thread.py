
def claim_worker_thread(
    backend_class: type[AsyncBackend], token: object
) -> Generator[Any, None, None]:
    from ..lowlevel import EventLoopToken

    threadlocals.current_token = EventLoopToken(backend_class, token)
    try:
        yield
    finally:
        del threadlocals.current_token

