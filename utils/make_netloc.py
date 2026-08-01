
def make_netloc(
    user: str | None,
    password: str | None,
    host: str | None,
    port: int | None,
    encode: bool = False,
) -> str:
    """Make netloc from parts.

    The user and password are encoded if encode is True.

    The host must already be encoded with _encode_host.
    """
    if host is None:
        return ""
    ret = host
    if port is not None:
        ret = f"{ret}:{port}"
    if user is None and password is None:
        return ret
    if password is not None:
        if not user:
            user = ""
        elif encode:
            user = QUOTER(user)
        if encode:
            password = QUOTER(password)
        user = f"{user}:{password}"
    elif user and encode:
        user = QUOTER(user)
    return f"{user}@{ret}" if user else ret

