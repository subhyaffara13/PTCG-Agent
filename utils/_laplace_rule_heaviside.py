
def _laplace_rule_heaviside(f, t, s):
    """
    This function deals with time-shifted Heaviside step functions. If the time
    shift is positive, it applies the time-shift rule of the Laplace transform.
    For example, if it gets ``(Heaviside(t-a)*f(t), t, s)``, it will compute
    ``exp(-a*s)*LaplaceTransform(f(t+a), t, s)``.

    If the time shift is negative, the Heaviside function is simply removed
    as it means nothing to the Laplace transform.

    The function does not remove a factor ``Heaviside(t)``; this is done by
    the simple rules.
    """

    a = Wild('a', exclude=[t])
    y = Wild('y')
    g = Wild('g')
    if ma1 := f.match(Heaviside(y) * g):
        if ma2 := ma1[y].match(t - a):
            if ma2[a].is_positive:
                _debug('     rule: time shift (4.1.4)')
                r, pr, cr = _laplace_transform(
                    ma1[g].subs(t, t + ma2[a]), t, s, simplify=False)
                return (exp(-ma2[a] * s) * r, pr, cr)
            if ma2[a].is_negative:
                _debug(
                    '     rule: Heaviside factor; negative time shift (4.1.4)')
                r, pr, cr = _laplace_transform(ma1[g], t, s, simplify=False)
                return (r, pr, cr)
        if ma2 := ma1[y].match(a - t):
            if ma2[a].is_positive:
                _debug('     rule: Heaviside window open')
                r, pr, cr = _laplace_transform(
                    (1 - Heaviside(t - ma2[a])) * ma1[g], t, s, simplify=False)
                return (r, pr, cr)
            if ma2[a].is_negative:
                _debug('     rule: Heaviside window closed')
                return (0, 0, S.true)
    return None

