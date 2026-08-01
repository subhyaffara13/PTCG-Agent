
def has_einsum(backend: str) -> bool:
    """Check if ``{backend}.einsum`` exists, cache result for performance."""
    try:
        return _has_einsum[backend]
    except KeyError:
        try:
            get_func("einsum", backend)
            _has_einsum[backend] = True
        except AttributeError:
            _has_einsum[backend] = False

        return _has_einsum[backend]

