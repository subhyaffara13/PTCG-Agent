
def phase_margin(system):
    r"""
    Returns the phase margin of a continuous time system.
    Only applicable to Transfer Functions which can generate valid bode plots.

    Raises
    ======

    NotImplementedError
        When time delay terms are present in the system.

    ValueError
        When a SISO LTI system is not passed.

        When more than one free symbol is present in the system.
        The only variable in the transfer function should be
        the variable of the Laplace transform.

    Examples
    ========

    >>> from sympy.physics.control import TransferFunction, phase_margin
    >>> from sympy.abc import s

    >>> tf = TransferFunction(1, s**3 + 2*s**2 + s, s)
    >>> phase_margin(tf)
    180*(-pi + atan((-1 + (-2*18**(1/3)/(9 + sqrt(93))**(1/3) + 12**(1/3)*(9 + sqrt(93))**(1/3))**2/36)/(-12**(1/3)*(9 + sqrt(93))**(1/3)/3 + 2*18**(1/3)/(3*(9 + sqrt(93))**(1/3)))))/pi + 180
    >>> phase_margin(tf).n()
    21.3863897518751

    >>> tf1 = TransferFunction(s**3, s**2 + 5*s, s)
    >>> phase_margin(tf1)
    -180 + 180*(atan(sqrt(2)*(-51/10 - sqrt(101)/10)*sqrt(1 + sqrt(101))/(2*(sqrt(101)/2 + 51/2))) + pi)/pi
    >>> phase_margin(tf1).n()
    -25.1783920627277

    >>> tf2 = TransferFunction(1, s + 1, s)
    >>> phase_margin(tf2)
    -180

    See Also
    ========

    gain_margin

    References
    ==========

    .. [1] https://en.wikipedia.org/wiki/Phase_margin

    """
    from sympy.functions import arg

    if not isinstance(system, SISOLinearTimeInvariant):
        raise ValueError("Margins are only applicable for SISO LTI systems.")

    _w = Dummy("w", real=True)
    repl = I*_w
    expr = system.to_expr()
    len_free_symbols = len(expr.free_symbols)
    if expr.has(exp):
        raise NotImplementedError("Margins for systems with Time delay terms are not supported.")
    elif len_free_symbols > 1:
        raise ValueError("Extra degree of freedom found. Make sure"
            " that there are no free symbols in the dynamical system other"
            " than the variable of Laplace transform.")

    w_expr = expr.subs({system.var: repl})

    mag = 20*log(Abs(w_expr), 10)
    mag_sol = list(solveset(mag, _w, Interval(0, oo, left_open=True)))

    if (len(mag_sol) == 0):
        pm = S(-180)
    else:
        wcp = mag_sol[0]
        pm = ((arg(w_expr)*S(180)/pi).subs({_w:wcp}) + S(180)) % 360

    if(pm >= 180):
        pm = pm - 360

    return pm

