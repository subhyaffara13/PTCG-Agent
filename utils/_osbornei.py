
def _osbornei(e, d):
    """Replace all trig functions with hyperbolic functions using
    the Osborne rule.

    Notes
    =====

    ``d`` is a dummy variable to prevent automatic evaluation
    of trigonometric/hyperbolic functions.

    References
    ==========

    .. [1] https://en.wikipedia.org/wiki/Hyperbolic_function
    """

    def f(rv):
        if not isinstance(rv, TrigonometricFunction):
            return rv
        const, x = rv.args[0].as_independent(d, as_Add=True)
        a = x.xreplace({d: S.One}) + const*I
        if isinstance(rv, sin):
            return sinh(a)/I
        elif isinstance(rv, cos):
            return cosh(a)
        elif isinstance(rv, tan):
            return tanh(a)/I
        elif isinstance(rv, cot):
            return coth(a)*I
        elif isinstance(rv, sec):
            return sech(a)
        elif isinstance(rv, csc):
            return csch(a)*I
        else:
            raise NotImplementedError('unhandled %s' % rv.func)

    return bottom_up(e, f)

