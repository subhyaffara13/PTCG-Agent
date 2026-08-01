
def _simplify_delta(expr):
    """
    Rewrite a KroneckerDelta's indices in its simplest form.
    """
    if isinstance(expr, KroneckerDelta):
        try:
            slns = solve(expr.args[0] - expr.args[1], dict=True)
            if slns and len(slns) == 1:
                return Mul(*[KroneckerDelta(*(key, value))
                            for key, value in slns[0].items()])
        except NotImplementedError:
            pass
    return expr

