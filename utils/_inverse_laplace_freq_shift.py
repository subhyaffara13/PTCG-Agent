
def _inverse_laplace_freq_shift(F, s, t, plane):
    """
    Helper function for the class InverseLaplaceTransform.
    """
    if not F.has(s):
        return F*DiracDelta(t), S.true
    if len(args := F.args) == 1:
        a = Wild('a', exclude=[s])
        if (ma := args[0].match(s-a)) and re(ma[a]).is_positive:
            _debug('     rule: F(s-a) o---o exp(-a*t)*f(t)')
            return (
                exp(-ma[a]*t) *
                InverseLaplaceTransform(F.func(s), s, t, plane), S.true)
    return None

