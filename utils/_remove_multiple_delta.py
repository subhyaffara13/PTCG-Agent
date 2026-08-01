
def _remove_multiple_delta(expr):
    """
    Evaluate products of KroneckerDelta's.
    """
    if expr.is_Add:
        return expr.func(*list(map(_remove_multiple_delta, expr.args)))
    if not expr.is_Mul:
        return expr
    eqs = []
    newargs = []
    for arg in expr.args:
        if isinstance(arg, KroneckerDelta):
            eqs.append(arg.args[0] - arg.args[1])
        else:
            newargs.append(arg)
    if not eqs:
        return expr
    solns = solve(eqs, dict=True)
    if len(solns) == 0:
        return S.Zero
    elif len(solns) == 1:
        newargs += [KroneckerDelta(k, v) for k, v in solns[0].items()]
        expr2 = expr.func(*newargs)
        if expr != expr2:
            return _remove_multiple_delta(expr2)
    return expr

