
def _laplace_rule_trig(fn, t_, s):
    """
    This rule covers trigonometric factors by splitting everything into a
    sum of exponential functions and collecting complex conjugate poles and
    real symmetric poles.
    """
    t = Dummy('t', real=True)

    if not fn.has(sin, cos, sinh, cosh):
        return None

    f, g = _laplace_trig_split(fn.subs(t_, t))
    xm, xn = _laplace_trig_expsum(f, t)

    if len(xn) > 0:
        # TODO not implemented yet, but also not important
        return None

    if not g.has(t):
        r, p = _laplace_trig_ltex(xm, t, s)
        return g*r, p, S.true
    else:
        # Just transform `g` and make frequency-shifted copies
        planes = []
        results = []
        G, G_plane, G_cond = _laplace_transform(g, t, s, simplify=False)
        for x1 in xm:
            results.append(x1['k']*G.subs(s, s-x1['a']))
            planes.append(G_plane+re(x1['a']))
    return Add(*results).subs(t, t_), Max(*planes), G_cond

