
def _has_binary_buffer(
    stream: t.BinaryIO | t.TextIO,
) -> t.TypeGuard[_BufferedTextPagerStream]:
    # TextIO is wider than TextIOWrapper; text-only streams such as StringIO
    # are valid TextIO values but do not expose a binary buffer to wrap.
    return getattr(stream, "buffer", None) is not None

