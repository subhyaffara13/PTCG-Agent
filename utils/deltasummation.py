
def deltasummation(f, limit, no_piecewise=False):
    """
    Handle summations containing a KroneckerDelta.

    Explanation
    ===========

    The idea for summation is the following:

    - If we are dealing with a KroneckerDelta expression, i.e. KroneckerDelta(g(x), j),
      we try to simplify it.

      If we could simplify it, then we sum the resulting expression.
      We already know we can sum a simplified expression, because only
      simple KroneckerDelta expressions are involved.

      If we could not simplify it, there are two cases:

      1) The expression is a simple expression: we return the summation,
         taking care if we are dealing with a Derivative or with a proper
         KroneckerDelta.

      2) The expression is not simple (i.e. KroneckerDelta(cos(x))): we can do
         nothing at all.

    - If the expr is a multiplication expr having a KroneckerDelta term:

      First we expand it.

      If the expansion did work, then we try to sum the expansion.

      If not, we try to extract a simple KroneckerDelta term, then we have two
      cases:

      1) We have a simple KroneckerDelta term, so we return the summation.

      2) We did not have a simple term, but we do have an expression with
         simplified KroneckerDelta terms, so we sum this expression.

    Examples
    ========

    >>> from sympy import oo, symbols
    >>> from sympy.abc import k
    >>> i, j = symbols('i, j', integer=True, finite=True)
    >>> from sympy.concrete.delta import deltasummation
    >>> from sympy import KroneckerDelta
    >>> deltasummation(KroneckerDelta(i, k), (k, -oo, oo))
    1
    >>> deltasummation(KroneckerDelta(i, k), (k, 0, oo))
    Piecewise((1, i >= 0), (0, True))
    >>> deltasummation(KroneckerDelta(i, k), (k, 1, 3))
    Piecewise((1, (i >= 1) & (i <= 3)), (0, True))
    >>> deltasummation(k*KroneckerDelta(i, j)*KroneckerDelta(j, k), (k, -oo, oo))
    j*KroneckerDelta(i, j)
    >>> deltasummation(j*KroneckerDelta(i, j), (j, -oo, oo))
    i
    >>> deltasummation(i*KroneckerDelta(i, j), (i, -oo, oo))
    j

    See Also
    ========

    deltaproduct
    sympy.functions.special.tensor_functions.KroneckerDelta
    sympy.concrete.sums.summation
    """
    if ((limit[2] - limit[1]) < 0) == True:
        return S.Zero

    if not f.has(KroneckerDelta):
        return summation(f, limit)

    x = limit[0]

    g = _expand_delta(f, x)
    if g.is_Add:
        return piecewise_fold(
            g.func(*[deltasummation(h, limit, no_piecewise) for h in g.args]))

    # try to extract a simple KroneckerDelta term
    delta, expr = _extract_delta(g, x)

    if (delta is not None) and (delta.delta_range is not None):
        dinf, dsup = delta.delta_range
        if (limit[1] - dinf <= 0) == True and (limit[2] - dsup >= 0) == True:
            no_piecewise = True

    if not delta:
        return summation(f, limit)

    solns = solve(delta.args[0] - delta.args[1], x)
    if len(solns) == 0:
        return S.Zero
    elif len(solns) != 1:
        return Sum(f, limit)
    value = solns[0]
    if no_piecewise:
        return expr.subs(x, value)
    return Piecewise(
        (expr.subs(x, value), Interval(*limit[1:3]).as_relational(value)),
        (S.Zero, True)
    )

