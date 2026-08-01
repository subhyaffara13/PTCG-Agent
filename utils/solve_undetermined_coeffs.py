
def solve_undetermined_coeffs(equ, coeffs, *syms, **flags):
    r"""
    Solve a system of equations in $k$ parameters that is formed by
    matching coefficients in variables ``coeffs`` that are on
    factors dependent on the remaining variables (or those given
    explicitly by ``syms``.

    Explanation
    ===========

    The result of this function is a dictionary with symbolic values of those
    parameters with respect to coefficients in $q$ -- empty if there
    is no solution or coefficients do not appear in the equation -- else
    None (if the system was not recognized). If there is more than one
    solution, the solutions are passed as a list. The output can be modified using
    the same semantics as for `solve` since the flags that are passed are sent
    directly to `solve` so, for example the flag ``dict=True`` will always return a list
    of solutions as dictionaries.

    This function accepts both Equality and Expr class instances.
    The solving process is most efficient when symbols are specified
    in addition to parameters to be determined,  but an attempt to
    determine them (if absent) will be made. If an expected solution is not
    obtained (and symbols were not specified) try specifying them.

    Examples
    ========

    >>> from sympy import Eq, solve_undetermined_coeffs
    >>> from sympy.abc import a, b, c, h, p, k, x, y

    >>> solve_undetermined_coeffs(Eq(a*x + a + b, x/2), [a, b], x)
    {a: 1/2, b: -1/2}
    >>> solve_undetermined_coeffs(a - 2, [a])
    {a: 2}

    The equation can be nonlinear in the symbols:

    >>> X, Y, Z = y, x**y, y*x**y
    >>> eq = a*X + b*Y + c*Z - X - 2*Y - 3*Z
    >>> coeffs = a, b, c
    >>> syms = x, y
    >>> solve_undetermined_coeffs(eq, coeffs, syms)
    {a: 1, b: 2, c: 3}

    And the system can be nonlinear in coefficients, too, but if
    there is only a single solution, it will be returned as a
    dictionary:

    >>> eq = a*x**2 + b*x + c - ((x - h)**2 + 4*p*k)/4/p
    >>> solve_undetermined_coeffs(eq, (h, p, k), x)
    {h: -b/(2*a), k: (4*a*c - b**2)/(4*a), p: 1/(4*a)}

    Multiple solutions are always returned in a list:

    >>> solve_undetermined_coeffs(a**2*x + b - x, [a, b], x)
    [{a: -1, b: 0}, {a: 1, b: 0}]

    Using flag ``dict=True`` (in keeping with semantics in :func:`~.solve`)
    will force the result to always be a list with any solutions
    as elements in that list.

    >>> solve_undetermined_coeffs(a*x - 2*x, [a], dict=True)
    [{a: 2}]
    """
    if not (coeffs and all(i.is_Symbol for i in coeffs)):
        raise ValueError('must provide symbols for coeffs')

    if isinstance(equ, Eq):
        eq = equ.lhs - equ.rhs
    else:
        eq = equ

    ceq = cancel(eq)
    xeq = _mexpand(ceq.as_numer_denom()[0], recursive=True)

    free = xeq.free_symbols
    coeffs = free & set(coeffs)
    if not coeffs:
        return ([], {}) if flags.get('set', None) else []  # solve(0, x) -> []

    if not syms:
        # e.g. A*exp(x) + B - (exp(x) + y) separated into parts that
        # don't/do depend on coeffs gives
        # -(exp(x) + y), A*exp(x) + B
        # then see what symbols are common to both
        # {x} = {x, A, B} - {x, y}
        ind, dep = xeq.as_independent(*coeffs, as_Add=True)
        dfree = dep.free_symbols
        syms = dfree & ind.free_symbols
        if not syms:
            # but if the system looks like (a + b)*x + b - c
            # then {} = {a, b, x} - c
            # so calculate {x} = {a, b, x} - {a, b}
            syms = dfree - set(coeffs)
        if not syms:
            syms = [Dummy()]
    else:
        if len(syms) == 1 and iterable(syms[0]):
            syms = syms[0]
        e, s, _ = recast_to_symbols([xeq], syms)
        xeq = e[0]
        syms = s

    # find the functional forms in which symbols appear

    gens = set(xeq.as_coefficients_dict(*syms).keys()) - {1}
    cset = set(coeffs)
    if any(g.has_xfree(cset) for g in gens):
        return  # a generator contained a coefficient symbol

    # make sure we are working with symbols for generators

    e, gens, _ = recast_to_symbols([xeq], list(gens))
    xeq = e[0]

    # collect coefficients in front of generators

    system = list(collect(xeq, gens, evaluate=False).values())

    # get a solution

    soln = solve(system, coeffs, **flags)

    # unpack unless told otherwise if length is 1

    settings = flags.get('dict', None) or flags.get('set', None)
    if type(soln) is dict or settings or len(soln) != 1:
        return soln
    return soln[0]

