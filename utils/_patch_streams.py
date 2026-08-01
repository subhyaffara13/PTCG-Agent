
def _patch_streams(out: TextIO) -> Iterator[None]:
    """Patch and subsequently reset a text stream."""
    sys.stderr = sys.stdout = out
    try:
        yield
    finally:
        sys.stderr = sys.__stderr__
        sys.stdout = sys.__stdout__

