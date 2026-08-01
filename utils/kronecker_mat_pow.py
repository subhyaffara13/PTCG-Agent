
def kronecker_mat_pow(expr):
    if isinstance(expr.base, KroneckerProduct) and all(a.is_square for a in expr.base.args):
        return KroneckerProduct(*[MatPow(a, expr.exp) for a in expr.base.args])
    else:
        return expr

