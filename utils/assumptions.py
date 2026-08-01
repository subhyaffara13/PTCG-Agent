
def assumptions(expr, _check=None):
    """return the T/F assumptions of ``expr``"""
    n = sympify(expr)
    if n.is_Symbol:
        rv = n.assumptions0  # are any important ones missing?
        if _check is not None:
            rv = {k: rv[k] for k in set(rv) & set(_check)}
        return rv
    rv = {}
    for k in _assume_defined if _check is None else _check:
        v = getattr(n, 'is_{}'.format(k))
        if v is not None:
            rv[k] = v
    return rv

