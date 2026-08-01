
def _laplace_rule_timescale(f, t, s):
    """
    This function applies the time-scaling rule of the Laplace transform in
    a straight-forward way. For example, if it gets ``(f(a*t), t, s)``, it will
    compute ``LaplaceTransform(f(t)/a, t, s/a)`` if ``a>0``.
    """

    a = Wild('a', exclude=[t])
    g = WildFunction('g', nargs=1)
    ma1 = f.match(g)
    if ma1:
        arg = ma1[g].args[0].collect(t)
        ma2 = arg.match(a*t)
        if ma2 and ma2[a].is_positive and ma2[a] != 1:
            _debug('     rule: time scaling (4.1.4)')
            r, pr, cr = _laplace_transform(
                1/ma2[a]*ma1[g].func(t), t, s/ma2[a], simplify=False)
            return (r, pr, cr)
    return None

