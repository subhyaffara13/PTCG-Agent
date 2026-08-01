
def has_tensordot(backend: str) -> bool:
    """Check if ``{backend}.tensordot`` exists, cache result for performance."""
    try:
        return _has_tensordot[backend]
    except KeyError:
        try:
            get_func("tensordot", backend)
            _has_tensordot[backend] = True
        except AttributeError:
            _has_tensordot[backend] = False

        return _has_tensordot[backend]

