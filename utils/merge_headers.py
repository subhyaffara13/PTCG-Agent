
def merge_headers(
    default_headers: typing.Sequence[tuple[bytes, bytes]] | None = None,
    override_headers: typing.Sequence[tuple[bytes, bytes]] | None = None,
) -> list[tuple[bytes, bytes]]:
    """
    Append default_headers and override_headers, de-duplicating if a key exists
    in both cases.
    """
    default_headers = [] if default_headers is None else list(default_headers)
    override_headers = [] if override_headers is None else list(override_headers)
    has_override = set(key.lower() for key, value in override_headers)
    default_headers = [
        (key, value)
        for key, value in default_headers
        if key.lower() not in has_override
    ]
    return default_headers + override_headers


def merge_headers(
    default_headers: typing.Sequence[tuple[bytes, bytes]] | None = None,
    override_headers: typing.Sequence[tuple[bytes, bytes]] | None = None,
) -> list[tuple[bytes, bytes]]:
    """
    Append default_headers and override_headers, de-duplicating if a key exists
    in both cases.
    """
    default_headers = [] if default_headers is None else list(default_headers)
    override_headers = [] if override_headers is None else list(override_headers)
    has_override = set(key.lower() for key, value in override_headers)
    default_headers = [
        (key, value)
        for key, value in default_headers
        if key.lower() not in has_override
    ]
    return default_headers + override_headers

