
def raise_on_deprecated():
    """Context manager to make DeprecationWarning raise an error

    This is to catch SymPyDeprecationWarning from library code while running
    tests and doctests. It is important to use this context manager around
    each individual test/doctest in case some tests modify the warning
    filters.
    """
    with warnings.catch_warnings():
        warnings.filterwarnings('error', '.*', DeprecationWarning, module='sympy.*')
        yield

