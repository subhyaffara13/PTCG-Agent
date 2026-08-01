
def is_partial_args(func, args, kwargs, sigspec=None):
    sigspec, rv = _check_sigspec(sigspec, func, _sigs._is_partial_args,
                                 func, args, kwargs)
    if sigspec is None:
        return rv
    try:
        sigspec.bind_partial(*args, **kwargs)
    except TypeError:
        return False
    return True

