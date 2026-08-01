
def singularities(expression, symbol, domain=None):
    """
    Find singularities of a given function.

    Parameters
    ==========

    expression : Expr
        The target function in which singularities need to be found.
    symbol : Symbol
        The symbol over the values of which the singularity in
        expression in being searched for.

    Returns
    =======

    Set
        A set of values for ``symbol`` for which ``expression`` has a
        singularity. An ``EmptySet`` is returned if ``expression`` has no
        singularities for any given value of ``Symbol``.

    Raises
    ======

    NotImplementedError
        Methods for determining the singularities of this function have
        not been developed.

    Notes
    =====

    This function does not find non-isolated singularities
    nor does it find branch points of the expression.

    Currently supported functions are:
        - univariate continuous (real or complex) functions

    References
    ==========

    .. [1] https://en.wikipedia.org/wiki/Mathematical_singularity

    Examples
    ========

    >>> from sympy import singularities, Symbol, log
    >>> x = Symbol('x', real=True)
    >>> y = Symbol('y', real=False)
    >>> singularities(x**2 + x + 1, x)
    EmptySet
    >>> singularities(1/(x + 1), x)
    {-1}
    >>> singularities(1/(y**2 + 1), y)
    {-I, I}
    >>> singularities(1/(y**3 + 1), y)
    {-1, 1/2 - sqrt(3)*I/2, 1/2 + sqrt(3)*I/2}
    >>> singularities(log(x), x)
    {0}

    """
    from sympy.solvers.solveset import solveset

    if domain is None:
        domain = S.Reals if symbol.is_real else S.Complexes
    try:
        sings = S.EmptySet
        e = expression.rewrite([sec, csc, cot, tan], cos)
        e = e.rewrite([sech, csch, coth, tanh], cosh)
        for i in e.atoms(Pow):
            if i.exp.is_infinite:
                raise NotImplementedError
            if i.exp.is_negative:
                # XXX: exponent of varying sign not handled
                sings += solveset(i.base, symbol, domain)
        for i in expression.atoms(log, asech, acsch):
            sings += solveset(i.args[0], symbol, domain)
        for i in expression.atoms(atanh, acoth):
            sings += solveset(i.args[0] - 1, symbol, domain)
            sings += solveset(i.args[0] + 1, symbol, domain)
        return sings
    except NotImplementedError:
        raise NotImplementedError(filldedent('''
            Methods for determining the singularities
            of this function have not been developed.'''))

