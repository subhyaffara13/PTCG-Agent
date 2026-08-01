
def request_context(
    request: Request | None = None,
) -> typing.Iterator[None]:
    """
    A context manager that can be used to attach the given request context
    to any `RequestError` exceptions that are raised within the block.
    """
    try:
        yield
    except RequestError as exc:
        if request is not None:
            exc.request = request
        raise exc

