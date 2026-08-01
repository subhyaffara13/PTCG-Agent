
def _basic_auth_no_warn(
    login: str, password: str = "", encoding: str = "latin1"
) -> BasicAuth:
    """Construct a BasicAuth without emitting the deprecation warning.

    For internal use only. Bypasses BasicAuth.__new__ so that aiohttp's own
    machinery doesn't trigger deprecation warnings in user code.
    """
    return tuple.__new__(BasicAuth, (login, password, encoding))

