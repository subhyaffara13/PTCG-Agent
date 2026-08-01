
def _inverse_laplace_time_shift(F, s, t, plane):
    """
    Helper function for the class InverseLaplaceTransform.
    """
    a = Wild('a', exclude=[s])
    g = Wild('g')

    if not F.has(s):
        return F*DiracDelta(t), S.true
    if not F.has(exp):
        return None

    ma1 = F.match(exp(a*s))
    if ma1:
        if ma1[a].is_negative:
            _debug('     rule: exp(-a*s) o---o DiracDelta(t-a)')
            return DiracDelta(t+ma1[a]), S.true
        else:
            return InverseLaplaceTransform(F, s, t, plane), S.true

    ma1 = F.match(exp(a*s)*g)
    if ma1:
        if ma1[a].is_negative:
            _debug('     rule: exp(-a*s)*F(s) o---o Heaviside(t-a)*f(t-a)')
            return _inverse_laplace_transform(
                ma1[g], s, t+ma1[a], plane, simplify=False, dorational=True)
        else:
            return InverseLaplaceTransform(F, s, t, plane), S.true
    return None

