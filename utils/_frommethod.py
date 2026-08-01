
def _frommethod(methodname: str, reversed: bool = False):
    """
    Define functions from existing MaskedArray methods.

    Parameters
    ----------
    methodname : str
        Name of the method to transform.
    reversed : bool, optional
        Whether to reverse the first two arguments of the method. Default is False.
    """
    method = getattr(MaskedArray, methodname)
    assert callable(method)

    signature = inspect.signature(method)
    params = list(signature.parameters.values())
    params[0] = params[0].replace(name="a")  # rename 'self' to 'a'

    if reversed:
        assert len(params) >= 2
        params[0], params[1] = params[1], params[0]

        def wrapper(a, b, *args, **params):
            return getattr(asanyarray(b), methodname)(a, *args, **params)

    else:
        def wrapper(a, *args, **params):
            return getattr(asanyarray(a), methodname)(*args, **params)

    wrapper.__signature__ = signature.replace(parameters=params)
    wrapper.__name__ = wrapper.__qualname__ = methodname

    # __doc__  is None when using `python -OO ...`
    if method.__doc__ is not None:
        str_signature = f"{methodname}{signature}"
        # TODO: For methods with a docstring "Parameters" section, that do not already
        # mention `a` (see e.g. `MaskedArray.var.__doc__`), it should be inserted there.
        wrapper.__doc__ = f"    {str_signature}\n{method.__doc__}"

    return wrapper

