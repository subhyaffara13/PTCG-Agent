
def gammasimp(expr):
    r"""
    Simplify expressions with gamma functions.

    Explanation
    ===========

    This function takes as input an expression containing gamma
    functions or functions that can be rewritten in terms of gamma
    functions and tries to minimize the number of those functions and
    reduce the size of their arguments.

    The algorithm works by rewriting all gamma functions as expressions
    involving rising factorials (Pochhammer symbols) and applies
    recurrence relations and other transformations applicable to rising
    factorials, to reduce their arguments, possibly letting the resulting
    rising factorial to cancel. Rising factorials with the second argument
    being an integer are expanded into polynomial forms and finally all
    other rising factorial are rewritten in terms of gamma functions.

    Then the following two steps are performed.

    1. Reduce the number of gammas by applying the reflection theorem
       gamma(x)*gamma(1-x) == pi/sin(pi*x).
    2. Reduce the number of gammas by applying the multiplication theorem
       gamma(x)*gamma(x+1/n)*...*gamma(x+(n-1)/n) == C*gamma(n*x).

    It then reduces the number of prefactors by absorbing them into gammas
    where possible and expands gammas with rational argument.

    All transformation rules can be found (or were derived from) here:

    .. [1] https://functions.wolfram.com/GammaBetaErf/Pochhammer/17/01/02/
    .. [2] https://functions.wolfram.com/GammaBetaErf/Pochhammer/27/01/0005/

    Examples
    ========

    >>> from sympy.simplify import gammasimp
    >>> from sympy import gamma, Symbol
    >>> from sympy.abc import x
    >>> n = Symbol('n', integer = True)

    >>> gammasimp(gamma(x)/gamma(x - 3))
    (x - 3)*(x - 2)*(x - 1)
    >>> gammasimp(gamma(n + 3))
    gamma(n + 3)

    """

    expr = expr.rewrite(gamma)

    # compute_ST will be looking for Functions and we don't want
    # it looking for non-gamma functions: issue 22606
    # so we mask free, non-gamma functions
    f = expr.atoms(Function)
    # take out gammas
    gammas = {i for i in f if isinstance(i, gamma)}
    if not gammas:
        return expr  # avoid side effects like factoring
    f -= gammas
    # keep only those without bound symbols
    f = f & expr.as_dummy().atoms(Function)
    if f:
        dum, fun, simp = zip(*[
            (Dummy(), fi, fi.func(*[
                _gammasimp(a, as_comb=False) for a in fi.args]))
            for fi in ordered(f)])
        d = expr.xreplace(dict(zip(fun, dum)))
        return _gammasimp(d, as_comb=False).xreplace(dict(zip(dum, simp)))

    return _gammasimp(expr, as_comb=False)

