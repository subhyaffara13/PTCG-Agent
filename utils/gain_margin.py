
def gain_margin(system):
    r"""
    Returns the gain margin of a continuous time system.
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

    >>> from sympy.physics.control import TransferFunction, gain_margin
    >>> from sympy.abc import s

    >>> tf = TransferFunction(1, s**3 + 2*s**2 + s, s)
    >>> gain_margin(tf)
    20*log(2)/log(10)
    >>> gain_margin(tf).n()
    6.02059991327962

    >>> tf1 = TransferFunction(s**3, s**2 + 5*s, s)
    >>> gain_margin(tf1)
    oo

    See Also
    ========

    phase_margin

    References
    ==========

    https://en.wikipedia.org/wiki/Bode_plot

    """
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
    phase = w_expr
    phase_sol = list(solveset(numer(phase.as_real_imag()[1].cancel()),_w, Interval(0, oo, left_open = True)))

    if (len(phase_sol) == 0):
        gm = oo
    else:
        wcg = phase_sol[0]
        gm = -mag.subs({_w:wcg})

    return gm

