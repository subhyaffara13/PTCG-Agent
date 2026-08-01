
def _get_windows_console_stream(
    f: t.TextIO, encoding: str | None, errors: str | None
) -> t.TextIO | None:
    if (
        get_buffer is None
        or encoding not in {"utf-16-le", None}
        or errors not in {"strict", None}
        or not _is_console(f)
    ):
        return None

    func = _stream_factories.get(f.fileno())
    if func is None:
        return None

    b = getattr(f, "buffer", None)

    if b is None:
        return None

    return func(b)

