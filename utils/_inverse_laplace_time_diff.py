
def _inverse_laplace_time_diff(F, s, t, plane):
    """
    Helper function for the class InverseLaplaceTransform.
    """
    n = Wild('n', exclude=[s])
    g = Wild('g')

    ma1 = F.match(s**n*g)
    if ma1 and ma1[n].is_integer and ma1[n].is_positive:
        _debug('     rule: s**n*F(s) o---o diff(f(t), t, n)')
        r, c = _inverse_laplace_transform(
            ma1[g], s, t, plane, simplify=False, dorational=True)
        r = r.replace(Heaviside(t), 1)
        if r.has(InverseLaplaceTransform):
            return diff(r, t, ma1[n]), c
        else:
            return Heaviside(t)*diff(r, t, ma1[n]), c
    return None

