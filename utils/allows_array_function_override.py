
def allows_array_function_override(func):
    """Determine if a Numpy function can be overridden via `__array_function__`

    Parameters
    ----------
    func : callable
        Function that may be overridable via `__array_function__`

    Returns
    -------
    bool
        `True` if `func` is a function in the Numpy API that is
        overridable via `__array_function__` and `False` otherwise.
    """
    return func in _array_functions

