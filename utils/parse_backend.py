
def parse_backend(arrays: Sequence[ArrayType], backend: Optional[str]) -> str:
    """Find out what backend we should use, dipatching based on the first
    array if ``backend='auto'`` is specified.
    """
    if (backend != "auto") and (backend is not None):
        return backend
    backend = infer_backend(arrays[0])

    # some arrays will be defined in modules that don't implement tensordot
    # etc. so instead default to numpy
    if not backends.has_tensordot(backend):
        return "numpy"

    return backend

