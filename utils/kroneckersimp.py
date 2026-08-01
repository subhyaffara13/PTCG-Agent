
def kroneckersimp(expr):
    """
    Simplify expressions with KroneckerDelta.

    The only simplification currently attempted is to identify multiplicative cancellation:

    Examples
    ========

    >>> from sympy import KroneckerDelta, kroneckersimp
    >>> from sympy.abc import i
    >>> kroneckersimp(1 + KroneckerDelta(0, i) * KroneckerDelta(1, i))
    1
    """
    def args_cancel(args1, args2):
        for i1 in range(2):
            for i2 in range(2):
                a1 = args1[i1]
                a2 = args2[i2]
                a3 = args1[(i1 + 1) % 2]
                a4 = args2[(i2 + 1) % 2]
                if Eq(a1, a2) is S.true and Eq(a3, a4) is S.false:
                    return True
        return False

    def cancel_kronecker_mul(m):
        args = m.args
        deltas = [a for a in args if isinstance(a, KroneckerDelta)]
        for delta1, delta2 in subsets(deltas, 2):
            args1 = delta1.args
            args2 = delta2.args
            if args_cancel(args1, args2):
                return S.Zero * m # In case of oo etc
        return m

    if not expr.has(KroneckerDelta):
        return expr

    if expr.has(Piecewise):
        expr = expr.rewrite(KroneckerDelta)

    newexpr = expr
    expr = None

    while newexpr != expr:
        expr = newexpr
        newexpr = expr.replace(lambda e: isinstance(e, Mul), cancel_kronecker_mul)

    return expr

