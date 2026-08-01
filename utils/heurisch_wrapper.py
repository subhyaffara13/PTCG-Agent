
def heurisch_wrapper(f, x, rewrite=False, hints=None, mappings=None, retries=3,
                     degree_offset=0, unnecessary_permutations=None,
                     _try_heurisch=None):
    """
    A wrapper around the heurisch integration algorithm.

    Explanation
    ===========

    This method takes the result from heurisch and checks for poles in the
    denominator. For each of these poles, the integral is reevaluated, and
    the final integration result is given in terms of a Piecewise.

    Examples
    ========

    >>> from sympy import cos, symbols
    >>> from sympy.integrals.heurisch import heurisch, heurisch_wrapper
    >>> n, x = symbols('n x')
    >>> heurisch(cos(n*x), x)
    sin(n*x)/n
    >>> heurisch_wrapper(cos(n*x), x)
    Piecewise((sin(n*x)/n, Ne(n, 0)), (x, True))

    See Also
    ========

    heurisch
    """
    from sympy.solvers.solvers import solve, denoms
    f = sympify(f)
    if not f.has_free(x):
        return f*x

    res = heurisch(f, x, rewrite, hints, mappings, retries, degree_offset,
                   unnecessary_permutations, _try_heurisch)
    if not isinstance(res, Basic):
        return res

    # We consider each denominator in the expression, and try to find
    # cases where one or more symbolic denominator might be zero. The
    # conditions for these cases are stored in the list slns.
    #
    # Since denoms returns a set we use ordered. This is important because the
    # ordering of slns determines the order of the resulting Piecewise so we
    # need a deterministic order here to make the output deterministic.
    slns = []
    for d in ordered(denoms(res)):
        try:
            slns += solve([d], dict=True, exclude=(x,))
        except NotImplementedError:
            pass
    if not slns:
        return res
    slns = list(uniq(slns))
    # Remove the solutions corresponding to poles in the original expression.
    slns0 = []
    for d in denoms(f):
        try:
            slns0 += solve([d], dict=True, exclude=(x,))
        except NotImplementedError:
            pass
    slns = [s for s in slns if s not in slns0]
    if not slns:
        return res
    if len(slns) > 1:
        eqs = []
        for sub_dict in slns:
            eqs.extend([Eq(key, value) for key, value in sub_dict.items()])
        slns = solve(eqs, dict=True, exclude=(x,)) + slns
    # For each case listed in the list slns, we reevaluate the integral.
    pairs = []
    for sub_dict in slns:
        expr = heurisch(f.subs(sub_dict), x, rewrite, hints, mappings, retries,
                        degree_offset, unnecessary_permutations,
                        _try_heurisch)
        cond = And(*[Eq(key, value) for key, value in sub_dict.items()])
        generic = Or(*[Ne(key, value) for key, value in sub_dict.items()])
        if expr is None:
            expr = integrate(f.subs(sub_dict),x)
        pairs.append((expr, cond))
    # If there is one condition, put the generic case first. Otherwise,
    # doing so may lead to longer Piecewise formulas
    if len(pairs) == 1:
        pairs = [(heurisch(f, x, rewrite, hints, mappings, retries,
                              degree_offset, unnecessary_permutations,
                              _try_heurisch),
                              generic),
                 (pairs[0][0], True)]
    else:
        pairs.append((heurisch(f, x, rewrite, hints, mappings, retries,
                              degree_offset, unnecessary_permutations,
                              _try_heurisch),
                              True))
    return Piecewise(*pairs)

