
def _make_axis_parameter_optional(init_func):
    """
    Decorator to allow leaving out the *axis* parameter in scale constructors.

    This decorator ensures backward compatibility for scale classes that
    previously required an *axis* parameter. It allows constructors to be
    called with or without the *axis* parameter.

    For simplicity, this does not handle the case when *axis*
    is passed as a keyword. However,
    scanning GitHub, there's no evidence that that is used anywhere.

    Parameters
    ----------
    init_func : callable
        The original __init__ method of a scale class.

    Returns
    -------
    callable
        A wrapped version of *init_func* that handles the optional *axis*.

    Notes
    -----
    If the wrapped constructor defines *axis* as its first argument, the
    parameter is preserved when present. Otherwise, the value `None` is injected
    as the first argument.

    Examples
    --------
    >>> from matplotlib.scale import ScaleBase
    >>> class CustomScale(ScaleBase):
    ...     @_make_axis_parameter_optional
    ...     def __init__(self, axis, custom_param=1):
    ...         self.custom_param = custom_param
    """
    @wraps(init_func)
    def wrapper(self, *args, **kwargs):
        sig = inspect.signature(init_func)
        try:
            # Try old signature.
            sig.bind(self, *args, **kwargs)
        except TypeError:
            # Use the new signature and pass in an unused axis=None.
            init_func(self, None, *args, **kwargs)
        else:
            # Use the old signature.
            init_func(self, *args, **kwargs)
    return wrapper

