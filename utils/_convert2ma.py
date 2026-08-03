import functools

def _convert2ma(funcname: str, np_ret: str, np_ma_ret: str,
                params: dict[str, str] | None = None):
    """Convert function from numpy to numpy.ma."""
    func = getattr(np, funcname)
    params = params or {}

    @functools.wraps(func, assigned=set(functools.WRAPPER_ASSIGNMENTS) - {"__module__"})
    def wrapper(*args, **kwargs):
        common_params = kwargs.keys() & params.keys()
        extras = params | {p: kwargs.pop(p) for p in common_params}

        result = func.__call__(*args, **kwargs).view(MaskedArray)

        if "fill_value" in common_params:
            result.fill_value = extras["fill_value"]
        if "hardmask" in common_params:
            result._hardmask = bool(extras["hardmask"])

        return result

    # workaround for a doctest bug in Python 3.11 that incorrectly assumes `__code__`
    # exists on wrapped functions
    del wrapper.__wrapped__

    # `arange`, `empty`, `empty_like`, `frombuffer`, and `zeros` have no signature
    try:
        signature = inspect.signature(func)
    except ValueError:
        signature = inspect.Signature([
            inspect.Parameter('args', inspect.Parameter.VAR_POSITIONAL),
            inspect.Parameter('kwargs', inspect.Parameter.VAR_KEYWORD),
        ])

    if params:
        sig_params = list(signature.parameters.values())

        # pop `**kwargs` if present
        sig_kwargs = None
        if sig_params[-1].kind is inspect.Parameter.VAR_KEYWORD:
            sig_kwargs = sig_params.pop()

        # add new keyword-only parameters
        for param_name, default in params.items():
            new_param = inspect.Parameter(
                param_name,
                inspect.Parameter.KEYWORD_ONLY,
                default=default,
            )
            sig_params.append(new_param)

        # re-append `**kwargs` if it was present
        if sig_kwargs:
            sig_params.append(sig_kwargs)

        signature = signature.replace(parameters=sig_params)

    wrapper.__signature__ = signature

    # __doc__  is None when using `python -OO ...`
    if func.__doc__ is not None:
        assert np_ret in func.__doc__, (
            f"Failed to replace `{np_ret}` with `{np_ma_ret}`. "
            f"The documentation string for return type, {np_ret}, is not "
            f"found in the docstring for `np.{func.__name__}`. "
            f"Fix the docstring for `np.{func.__name__}` or "
            "update the expected string for return type."
        )
        wrapper.__doc__ = inspect.cleandoc(func.__doc__).replace(np_ret, np_ma_ret)

    return wrapper

