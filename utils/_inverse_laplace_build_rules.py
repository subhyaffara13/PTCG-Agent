
def _inverse_laplace_build_rules():
    """
    This is an internal helper function that returns the table of inverse
    Laplace transform rules in terms of the time variable `t` and the
    frequency variable `s`.  It is used by `_inverse_laplace_apply_rules`.
    """
    s = Dummy('s')
    t = Dummy('t')
    a = Wild('a', exclude=[s])
    b = Wild('b', exclude=[s])
    c = Wild('c', exclude=[s])

    _debug('_inverse_laplace_build_rules is building rules')

    def _frac(f, s):
        try:
            return f.factor(s)
        except PolynomialError:
            return f

    def same(f): return f
    # This list is sorted according to the prep function needed.
    _ILT_rules = [
        (a/s, a, S.true, same, 1),
        (
            b*(s+a)**(-c), t**(c-1)*exp(-a*t)/gamma(c),
            S.true, same, 1),
        (1/(s**2+a**2)**2, (sin(a*t) - a*t*cos(a*t))/(2*a**3),
         S.true, same, 1),
        # The next two rules must be there in that order. For the second
        # one, the condition would be a != 0 or, respectively, to take the
        # limit a -> 0 after the transform if a == 0. It is much simpler if
        # the case a == 0 has its own rule.
        (1/(s**b), t**(b - 1)/gamma(b), S.true, same, 1),
        (1/(s*(s+a)**b), lowergamma(b, a*t)/(a**b*gamma(b)),
         S.true, same, 1)
    ]
    return _ILT_rules, s, t

