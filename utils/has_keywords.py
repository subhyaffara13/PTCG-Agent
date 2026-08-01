
def has_keywords(func, sigspec=None):
    sigspec, rv = _check_sigspec(sigspec, func, _sigs._has_keywords, func)
    if sigspec is None:
        return rv
    return any(p.default is not p.empty
               or p.kind in (p.KEYWORD_ONLY, p.VAR_KEYWORD)
               for p in sigspec.parameters.values())

