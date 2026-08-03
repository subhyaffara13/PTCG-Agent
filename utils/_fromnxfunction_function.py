import functools

def _fromnxfunction_function(_fromnxfunction):
    """
    Decorator to wrap a "_fromnxfunction" function, wrapping a numpy function as a
    masked array function, with proper docstring and name.

    Parameters
    ----------
    _fromnxfunction : ({params}) -> ndarray, {params}) -> masked_array
        Wrapper function that calls the wrapped numpy function

    Returns
    -------
    decorator : (f: ({params}) -> ndarray) -> ({params}) -> masked_array
        Function that accepts a numpy function and returns a masked array function

    """
    def decorator(npfunc, /):
        def wrapper(*args, **kwargs):
            return _fromnxfunction(npfunc, *args, **kwargs)

        functools.update_wrapper(wrapper, npfunc, assigned=("__name__", "__qualname__"))
        wrapper.__doc__ = ma.doc_note(
            npfunc.__doc__,
            "The function is applied to both the ``_data`` and the ``_mask``, if any.",
        )
        return wrapper

    return decorator

