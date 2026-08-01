
def is_anyio_cancellation(exc: CancelledError) -> bool:
    # Sometimes third party frameworks catch a CancelledError and raise a new one, so as
    # a workaround we have to look at the previous ones in __context__ too for a
    # matching cancel message
    while True:
        if (
            exc.args
            and isinstance(exc.args[0], str)
            and exc.args[0].startswith("Cancelled via cancel scope ")
        ):
            return True

        if isinstance(exc.__context__, CancelledError):
            exc = exc.__context__
            continue

        return False

