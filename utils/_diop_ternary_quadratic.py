
def _diop_ternary_quadratic(_var, coeff):
    eq = sum(i*coeff[i] for i in coeff)
    if HomogeneousTernaryQuadratic(eq).matches():
        return HomogeneousTernaryQuadratic(eq, free_symbols=_var).solve()
    elif HomogeneousTernaryQuadraticNormal(eq).matches():
        return HomogeneousTernaryQuadraticNormal(eq, free_symbols=_var).solve()

