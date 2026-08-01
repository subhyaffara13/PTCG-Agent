
def _inverse_laplace_diff(f, s, t, plane):
    """
    Helper function for the class InverseLaplaceTransform.
    """
    a = Wild('a', exclude=[s])
    n = Wild('n', exclude=[s])
    g = Wild('g')
    ma = f.match(a*Derivative(g, (s, n)))
    if ma and ma[n].is_integer:
        _debug('     rule: t**n*f(t) o---o (-1)**n*diff(F(s), s, n)')
        r, c = _inverse_laplace_transform(
            ma[g], s, t, plane, simplify=False, dorational=False)
        return (-t)**ma[n]*r, c
    return None

