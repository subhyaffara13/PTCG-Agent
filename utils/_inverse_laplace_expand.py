
def _inverse_laplace_expand(fn, s, t, plane):
    """
    Helper function for the class InverseLaplaceTransform.
    """
    if fn.is_Add:
        return None
    r = expand(fn, deep=False)
    if r.is_Add:
        return _inverse_laplace_transform(
            r, s, t, plane, simplify=False, dorational=True)
    r = expand_mul(fn)
    if r.is_Add:
        return _inverse_laplace_transform(
            r, s, t, plane, simplify=False, dorational=True)
    r = expand(fn)
    if r.is_Add:
        return _inverse_laplace_transform(
            r, s, t, plane, simplify=False, dorational=True)
    if fn.is_rational_function(s):
        r = fn.apart(s).doit()
    if r.is_Add:
        return _inverse_laplace_transform(
            r, s, t, plane, simplify=False, dorational=True)
    return None

