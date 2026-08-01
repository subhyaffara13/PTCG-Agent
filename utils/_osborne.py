
def _osborne(e, d):
    """Replace all hyperbolic functions with trig functions using
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
        if not isinstance(rv, HyperbolicFunction):
            return rv
        a = rv.args[0]
        a = a*d if not a.is_Add else Add._from_args([i*d for i in a.args])
        if isinstance(rv, sinh):
            return I*sin(a)
        elif isinstance(rv, cosh):
            return cos(a)
        elif isinstance(rv, tanh):
            return I*tan(a)
        elif isinstance(rv, coth):
            return cot(a)/I
        elif isinstance(rv, sech):
            return sec(a)
        elif isinstance(rv, csch):
            return csc(a)/I
        else:
            raise NotImplementedError('unhandled %s' % rv.func)

    return bottom_up(e, f)

