
def _iter_stdin(stream: IO[str]) -> Iterable[str]:
    """Yield non-empty stripped lines from ``stream``, ignoring blanks."""
    for line in stream:
        stripped = line.strip()
        if stripped:
            yield stripped

