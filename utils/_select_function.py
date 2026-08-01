
def _select_function(sort):
    if callable(sort):
        # assume the user knows what they're doing
        sfunction = sort
    elif sort == 'lhp':
        sfunction = _lhp
    elif sort == 'rhp':
        sfunction = _rhp
    elif sort == 'iuc':
        sfunction = _iuc
    elif sort == 'ouc':
        sfunction = _ouc
    else:
        raise ValueError("sort parameter must be None, a callable, or "
                         "one of ('lhp','rhp','iuc','ouc')")

    return sfunction

