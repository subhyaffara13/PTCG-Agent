
def _token_or_error(token: EventLoopToken | None) -> EventLoopToken:
    if token is not None:
        return token

    try:
        return threadlocals.current_token
    except AttributeError:
        raise NoEventLoopError(
            "Not running inside an AnyIO worker thread, and no event loop token was "
            "provided"
        ) from None

