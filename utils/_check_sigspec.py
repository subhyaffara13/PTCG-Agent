
def _check_sigspec(sigspec, func, builtin_func, *builtin_args):
    if sigspec is None:
        try:
            sigspec = inspect.signature(func)
        except (ValueError, TypeError) as e:
            sigspec = e
    if isinstance(sigspec, ValueError):
        return None, builtin_func(*builtin_args)
    elif not isinstance(sigspec, inspect.Signature):
        if (
            func in _sigs.signatures
            and (
                hasattr(func, '__signature__')
                and hasattr(func.__signature__, '__get__')
            )
        ):
            val = builtin_func(*builtin_args)
            return None, val
        return None, False
    return sigspec, None

