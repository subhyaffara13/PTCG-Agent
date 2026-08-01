
def hyper_as_trig(rv):
    """Return an expression containing hyperbolic functions in terms
    of trigonometric functions. Any trigonometric functions initially
    present are replaced with Dummy symbols and the function to undo
    the masking and the conversion back to hyperbolics is also returned. It
    should always be true that::

        t, f = hyper_as_trig(expr)
        expr == f(t)

    Examples
    ========

    >>> from sympy.simplify.fu import hyper_as_trig, fu
    >>> from sympy.abc import x
    >>> from sympy import cosh, sinh
    >>> eq = sinh(x)**2 + cosh(x)**2
    >>> t, f = hyper_as_trig(eq)
    >>> f(fu(t))
    cosh(2*x)

    References
    ==========

    .. [1] https://en.wikipedia.org/wiki/Hyperbolic_function
    """
    from sympy.simplify.simplify import signsimp
    from sympy.simplify.radsimp import collect

    # mask off trig functions
    trigs = rv.atoms(TrigonometricFunction)
    reps = [(t, Dummy()) for t in trigs]
    masked = rv.xreplace(dict(reps))

    # get inversion substitutions in place
    reps = [(v, k) for k, v in reps]

    d = Dummy()

    return _osborne(masked, d), lambda x: collect(signsimp(
        _osbornei(x, d).xreplace(dict(reps))), S.ImaginaryUnit)

