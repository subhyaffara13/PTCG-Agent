
def get_pager_file(
    color: bool | None = None,
) -> t.ContextManager[t.TextIO]:
    """Context manager.

    Yields a writable file-like object which can be used as an output pager.

    .. versionadded:: 8.4.0

    :param color: controls if the pager supports ANSI colors or not.  The
                  default is autodetection.
    """
    from ._termui_impl import get_pager_file

    color = resolve_color_default(color)

    return get_pager_file(color=color)


def get_pager_file(color: bool | None = None) -> t.Generator[t.TextIO, None, None]:
    """Context manager.

    Yields a writable file-like object which can be used as an output pager.

    .. versionadded:: 8.4.0

    :param color: controls if the pager supports ANSI colors or not.  The
                  default is autodetection.
    """
    with _pager_contextmanager(color=color) as (stream, encoding, color):
        # Split streams by capabilities rather than the abstract TextIO /
        # BinaryIO annotations: buffered text streams can be unwrapped to bytes,
        # while other streams are yielded as-is.
        wrapper: MaybeStripAnsi | None = None
        if _has_binary_buffer(stream):
            # Text stream backed by a binary buffer.
            wrapper = MaybeStripAnsi(stream.buffer, color=color, encoding=encoding)
            stream = wrapper
        try:
            # Narrow the BinaryIO | TextIO union that _pager_contextmanager
            # yields; the caller writes text to the pager.
            yield t.cast(t.TextIO, stream)
        finally:
            try:
                stream.flush()
            finally:
                # Hand the binary buffer back to the pager that produced it
                # rather than letting this TextIOWrapper close it on garbage
                # collection. The pager owns the buffer's lifecycle: subprocess
                # pipes and temp files are closed by their own helpers, while a
                # borrowed stdout must stay open for the caller. detach() runs
                # even if flush() raised, so the buffer is never closed here.
                if wrapper is not None:
                    wrapper.detach()

