
def default_xp(xp: ModuleType) -> Generator[None, None, None]:
    """In all ``xp_assert_*`` and ``assert_*`` function calls executed within this
    context manager, test by default that the array namespace is
    the provided across all arrays, unless one explicitly passes the ``xp=``
    parameter or ``check_namespace=False``.

    Without this context manager, the default value for `xp` is the namespace
    for the desired array (the second parameter of the tests).
    """
    token = _default_xp_ctxvar.set(xp)
    try:
        yield
    finally:
        _default_xp_ctxvar.reset(token)

