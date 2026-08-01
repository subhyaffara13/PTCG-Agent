
def _nullpager(
    stream: t.TextIO, color: bool | None = None
) -> t.Iterator[tuple[t.TextIO, str, bool]]:
    """Simply print unformatted text. This is the ultimate fallback. Don't close the
    output stream in this case, since it's coming from elsewhere rather than our
    internal helpers.

    The stream is wrapped in :class:`~click.utils.KeepOpenFile` so that, as a
    borrowed stream, it is not closed by a ``with`` block. The wrapper that
    :func:`get_pager_file` builds around it is detached rather than closed.
    """
    encoding = get_best_encoding(stream)

    if color is None:
        color = False

    yield KeepOpenFile(stream), encoding, color  # type: ignore[misc]

