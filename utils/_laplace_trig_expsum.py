
def _laplace_trig_expsum(f, t):
    """
    Helper function for `_laplace_rule_trig`.  This function expects the `f`
    from `_laplace_trig_split`.  It returns two lists `xm` and `xn`.  `xm` is
    a list of dictionaries with keys `k` and `a` representing a function
    `k*exp(a*t)`.  `xn` is a list of all terms that cannot be brought into
    that form, which may happen, e.g., when a trigonometric function has
    another function in its argument.
    """
    c1 = Wild('c1', exclude=[t])
    c0 = Wild('c0', exclude=[t])
    p = Wild('p', exclude=[t])
    xm = []
    xn = []

    x1 = f.rewrite(exp).expand()

    for term in Add.make_args(x1):
        if not term.has(t):
            xm.append({'k': term, 'a': 0, re: 0, im: 0})
            continue
        term = _laplace_deep_collect(term.powsimp(combine='exp'), t)

        if (r := term.match(p*exp(c1*t+c0))) is not None:
            xm.append({
                'k': r[p]*exp(r[c0]), 'a': r[c1],
                re: re(r[c1]), im: im(r[c1])})
        else:
            xn.append(term)
    return xm, xn

