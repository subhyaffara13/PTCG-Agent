
def has_varargs(func, sigspec=None):
    sigspec, rv = _check_sigspec(sigspec, func, _sigs._has_varargs, func)
    if sigspec is None:
        return rv
    return any(p.kind == p.VAR_POSITIONAL
               for p in sigspec.parameters.values())

