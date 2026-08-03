import sys

def should_strip_ansi(
    stream: t.IO[t.Any] | None = None, color: bool | None = None
) -> bool:
    if color is None:
        if stream is None:
            stream = sys.stdin
        elif hasattr(stream, "color"):
            # ._termui_impl.MaybeStripAnsi handles stripping ansi itself,
            # so we don't need to strip it here
            return False
        return not isatty(stream) and not _is_jupyter_kernel_output(stream)
    return not color

