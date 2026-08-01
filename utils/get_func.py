
def get_func(func: str, backend: str = "numpy", default: Any = None) -> Any:
    """Return ``{backend}.{func}``, e.g. ``numpy.einsum``,
    or a default func if provided. Cache result.
    """
    try:
        return _cached_funcs[func, backend]
    except KeyError:
        fn = _import_func(func, backend, default)
        _cached_funcs[func, backend] = fn
        return fn

