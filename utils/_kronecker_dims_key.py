
def _kronecker_dims_key(expr):
    if isinstance(expr, KroneckerProduct):
        return tuple(a.shape for a in expr.args)
    else:
        return (0,)

