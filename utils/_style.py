
def _style(message: str, **kwargs: Any) -> str:
    """Wrapper around mypy.util for fancy formatting."""
    kwargs.setdefault("color", "none")
    return _formatter.style(message, **kwargs)


def _style(s, color):
    """Return color/style-formatted input `s` if `sys.stdout` is interactive, e.g. connected to a terminal."""
    if sys.stdout.isatty():
        return f"{PALETTE[color]}{s}{PALETTE['reset']}"
    else:
        return s

