
def enforce_stream(
    value: bytes | typing.Iterable[bytes] | typing.AsyncIterable[bytes] | None,
    *,
    name: str,
) -> typing.Iterable[bytes] | typing.AsyncIterable[bytes]:
    if value is None:
        return ByteStream(b"")
    elif isinstance(value, bytes):
        return ByteStream(value)
    return value

