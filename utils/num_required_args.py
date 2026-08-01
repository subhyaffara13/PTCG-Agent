
def num_required_args(func, sigspec=None):
    sigspec, rv = _check_sigspec(sigspec, func, _sigs._num_required_args,
                                 func)
    if sigspec is None:
        return rv
    return sum(1 for p in sigspec.parameters.values()
               if p.default is p.empty
               and p.kind in (p.POSITIONAL_OR_KEYWORD, p.POSITIONAL_ONLY))

